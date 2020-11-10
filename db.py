from datetime import *
import json
from json import dumps
from typing import *
import typing
import bson
from bson.objectid import ObjectId
from pymongo import *
from pymongo.cursor import *
from bson import json_util


class Database:
    def __init__(self, name, host="mongodb://localhost:27017/"):
        self.client = MongoClient(host)
        self.db = self.client[name]
        self.classes = {}
        Database.main = self

    def register(self, model):
        model.db = self
        model.col = self.db[model.__name__]
        self.classes[model.__name__] = model

    def wrap(self, name, input: Cursor or object, skip=0, limit=0) -> None or List[object] or object:
        if not input:
            return None
        Klass = self.getModel(name)
        if isinstance(input, Cursor):
            if skip != 0:
                input.skip(skip)
            if limit != 0:
                input.limit(limit)
            items = []
            for item in input:
                items.append(Klass(item))
            if skip != 0 or limit != 0:
                return {
                    "total": input.count(),
                    "rows": items
                }
            return items
        return Klass(input)

    def getModel(self, name) -> Type[object]:
        model = name
        if isinstance(name, str):
            model = self.classes[name]
        return model

    def getCollection(self, name) -> Collection:
        model = self.getModel(name)
        return model.col

    def findOne(self, name, criteria):
        return self.wrap(name, self.getCollection(name).find_one(criteria))

    def findMany(self, name, criteria):
        skip = 0
        limit = 0
        if "skip" in criteria:
            skip = criteria["skip"]
            del criteria["skip"]
        if "limit" in criteria:
            limit = criteria["limit"]
            del criteria["limit"]
        return self.wrap(name, self.getCollection(name).find(criteria), skip, limit)

    def updateMany(self, name, criteria, data):
        ret = self.getCollection(name).update_many(criteria, data)
        return self.wrap(name, ret.raw_result)

    def updateOne(self, name, criteria, data):
        ret = self.getCollection(name).update_one(criteria, data)
        return self.wrap(name, ret.raw_result)

    def deleteMany(self, name, criteria):
        ret = self.getCollection(name).delete_many(criteria)
        return self.wrap(name, ret.raw_result)

    def deleteOne(self, name, criteria):
        ret = self.getCollection(name).delete_one(criteria)
        return self.wrap(name, ret.raw_result)

    def save(self, name, data):
        model = self.getCollection(name)
        if isinstance(data, list):
            ret = model.insert_many(data)
            return self.findMany(name, {
                "_id": ret.inserted_ids
            })
        ret = model.insert_one(data)
        return self.findOne(name, {
            "_id": ret.inserted_id
        })

    def remove(self, name, data):
        model = self.getCollection(name)
        if isinstance(data, list):
            ids = []
            for item in data:
                ids.append(item._id)
            ret = model.delete_many({"_id": ids})
            return self.wrap(name, ret.raw_result)
        ret = model.delete_one({"_id": data._id})
        return self.wrap(name, ret.raw_result)

class Model:

    def newProp(name: str, default: Any = None, test: Callable[[Any, Any, Dict], None] or None = None, doc: (str or None) = None, hide: bool = False) -> property:
        def setProp(self, value):
            if test is not None:
                errs = self["errors"] or {}
                test(self, value, errs)
                self["errors"] = errs
            self[name] = value

        def getProp(self):
            item = self[name]
            if item is None and default is not None:
                self[name] = default
                return default
            return item

        def delProp(self):
            del self[name]

        prop = property(getProp, setProp, delProp, doc)
        #prop.__dict__["test"] = test
        #prop.__dict__["hide"] = hide
        return prop

    id = newProp(name="_id", doc="Unique idetification for database")
    _id = newProp(name="_id", doc="Unique idetification for database")
    created = newProp(name="created", doc="Datetime created")
    updated = newProp(name="updated", doc="Datetime updated")

    def items(self):
        return self.__data.items()

    def __delitem__(self, key: Any):
        del self.__data[key]

    def __getitem__(self, key: Any):
        return self.__data.get(key)

    def __setitem__(self, key: Any, value: Any):
        self.__data[key] = value

    def __init__(self, data: Any):
        if isinstance(data, Model):
            self.__data = data.__data.copy()
        elif isinstance(data, dict):
            self.__data = dict()
            self.apply(data)
        else:
            self.__data = dict()

    def filter(self, user: Any) -> Any:
        data = self.__data.copy()
        if user is not None and user.admin:
            return data
        owners = [self.id]
        if "owners" in data and isinstance(data["owners"], list):
            owners.extend(data["owners"])
        # Override this to remove things based on user
        for key in self.items():
            hide = self[key].__dict__["hide"]
            if user:
                if hide and not self.isOwner(user):
                    del data[key]
            elif hide:
                del data[key]
        return data

    def valid(self) -> bool:
        return len(self.errors) == 0

    def isOwner(self, value: Any):
        id = None
        if isinstance(value, Model):
            id = value.id
        elif isinstance(value, str):
            id = value
        if id is not None:
            if self.id == id:
                return True
            if "owners" in self.__data:
                    owners = self["owners"]
                    if isinstance(owners, list):
                        return owners.count(id) >= 1
        return False

    def addOwner(self, value: Any):
        if "owners" not in self.__data:
            self.__data["owners"] = list()
        id = None
        if isinstance(value, Model):
            id = value.id
        elif isinstance(value, str):
            id = value
        if id is not None:
            owners = self["owners"]
            if isinstance(owners, list):
                owners.append(id)

    def removeOwner(self, value: Any):
        if "owners" in self.__data:
            id = None
            if isinstance(value, Model):
                id = value.id
            elif isinstance(value, str):
                id = value
            if id is not None:
                owners = self["owners"]
                if isinstance(owners, list):
                    owners.remove(id)

    def getDB(self):
        if Database.main is not None:
            return Database.main
        Klass = self.__class__
        while Klass is not None and Klass.db is not None:
            if Klass.db is not None:
                return Klass.db
            Klass = Klass.__class__
        return None

    def getModelName(self):
        return self.__class__.__name__

    def setResolve(data: dict, fieldMap: dict):
        if isinstance(data, dict):
            for field, FClass in fieldMap.items():
                nData = data.copy()
                for key, value in data.items():
                    if isinstance(key, str):
                        if key.startswith(field+'.'):
                            nKey = key[len(field)+1:]
                            if len(nKey) > 0:
                                nObj = nData.get(field, {})
                                nObj[nKey] = value
                                del nData[key]
                                nData[field] = nObj
                data = nData
                if field in data and isinstance(data[field], dict):
                    data[field] = FClass.resolve(data[field])
        return data

    def resolve(Class: Any, input: Any):
        if isinstance(input, object):
            item = Class.findOne(input)
            if not isinstance(item, Class):
                item = Class(input).save()
            if item:
                return item.id
            return item
        elif isinstance(input, dict):
            out = dict()
            for index, itemIn in input.items():
                out[index] = Class.resolve(itemIn)
            return out
        elif isinstance(input, list):
            out = []
            for index, itemIn in input:
                out.append(Class.resolve(itemIn))
            return out
        return input

    def apply(self, data: dict):
        if isinstance(data, dict):
            allowed = [attr for attr in dir(
                self) if not callable(getattr(self, attr))]
            for key, value in data.items():
                if allowed.count(key) >= 1:
                    self.__data[key] = value
        return self

    def save(self):
        if not self.valid():
            return None
        db = self.getDB()
        if db is not None:
            if "nonce" in self.__data:
                del self.__data["nonce"]
            if "_id" not in self.__data:
                self.created = datetime.now()
            self.updated = datetime.now()
            return self.apply(db.save(self.getModelName(), self.__data))
        return None

    def remove(self):
        db = self.getDB()
        if db is not None:
            return db.remove(self.getModelName(), self.__data)
        return None


def default(v: Any) -> Any:
    if isinstance(v, bson.ObjectId):
        return str(v)
    elif isinstance(v, datetime):
        return v.timestamp()
    elif isinstance(v, Model):
        return str(v)
    return v


def devListJSON(user: Model, request, ModelT: Type[Model], includes: List[Type[Model] or str]):
    sel = {"owners": {"$in": [user.id]}}
    if "limit" in request.args and int(request.args["limit"]) > 0:
        sel["limit"] = int(request.args["limit"])
    if "offset" in request.args and int(request.args["offset"]) > 0:
        sel["offset"] = int(request.args["offset"])
    if "search" in request.args and request.args["search"] != "":
        sel["$text"] = {
            "$search": request.args["search"],
            "$language": user.lang,
            "$caseSensitive": False,
            "$diacriticSensitive": False
        }
    items = ModelT.findMany(sel)
    rows = []
    resp = {}
    l = 0
    if "rows" in items:
        l = items["total"]
        for item in items["rows"]:
            rows.append(item.filter(user))
            item.setResponse(user, includes, resp)
    else:
        l = len(items)
        for item in items:
            rows.append(item.filter(user))
            item.setResponse(user, includes, resp)
    resp["total"] = l
    resp["rows"] = rows
    return json.dumps(resp, default=default), 200


def devSetResponse(fieldMap: Dict[str, str or Type[Model] or List[Type[Model] or str]]):
    def setResponse(self: Model, user: Any, include: List[str or Type[Model]], resp: Dict = {}):
        for fieldName, fieldType in fieldMap.items():
            if fieldName not in resp:
                resp[fieldName] = dict()
            respItems: Dict[str, Model] = resp[fieldName]
            if isinstance(fieldType, list):
                fClass: Type[Model] = fieldType[0]
                fClassName: str = ""
                if isinstance(fClass, str):
                    fClass = self.getDB().getModel(fClass)
                    fClassName: str = fClass.__name__
                else:
                    fClassName: str = fClass.__name__
                if fClass in include or fClassName in include:
                    items: List[Model] = fClass.findMany(
                        {"_id": self[fieldName]})
                    for item in items:
                        if hasattr(item, 'setResponse') and callable(getattr(item, 'setResponse')):
                            item.setResponse(user, include, resp)
                        else:
                            respItems[str(item.id)] = item.filter(user)
            elif isinstance(fieldType, str):
                fClass: Type[Model] = self.getDB().getModel(fieldType)
                fClassName: str = fClass.__name__
                if fClass in include or fClassName in include:
                    item: Model = fieldType.findOne({"_id": self[fieldName]})
                    if item:
                        if hasattr(item, 'setResponse') and callable(getattr(item, 'setResponse')):
                            item.setResponse(user, include, resp)
                        else:
                            respItems[str(item.id)] = item.filter(user)
            elif issubclass(fieldType, Model):
                fClass: Type[Model] = fieldType
                fClassName: str = fClass.__name__
                if fClass in include or fClassName in include:
                    item: Model = fieldType.findOne({"_id": self[fieldName]})
                    if item:
                        if hasattr(item, 'setResponse') and callable(getattr(item, 'setResponse')):
                            item.setResponse(user, include, resp)
                        else:
                            respItems[str(item.id)] = item.filter(user)
            resp[fieldName] = respItems
        return resp
    return setResponse

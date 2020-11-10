import { default as $, type } from "jquery";
import "bootstrap-table/src/bootstrap-table.scss";
import "bootstrap-table";
import luxon, { DateTime, Interval } from "luxon"; 

interface ModelInterface {
  _id: string;
  created: number | string;
  updated: number | string;
  [field: string]: any;
}

function parseElapsedDate(row: ModelInterface, field: string) {
  if (typeof(row[field]) == "number") {
    let then = DateTime.fromSeconds(Math.floor(row[field]));
    row[field] = then.toRelative();
  }
}

function parseModel(row: ModelInterface) {
  parseElapsedDate(row, "created");
  parseElapsedDate(row, "updated");
  return row;
}

function tableResponseHandler(res: any): any {
  let rows = (res.rows as Array<ModelInterface>);
  let maps = new Map<String, Map<String, ModelInterface>>();
  let allowed = ["rows", "total"];
  
  for (const key in res) {
    if (Object.prototype.hasOwnProperty.call(res, key)) {
      const value = res[key];
      if (allowed.indexOf(key) == -1) {
        let itemMap = new Map<String, ModelInterface>(Object.keys(value).map((id) => {
          return [id, parseModel(value[id])];
        }));
        maps.set(key, itemMap);
      }
    }
  }
  for (let i = 0; i < rows.length; i++) {
    const row = parseModel(rows[i]);
    maps.forEach((itemMap, fieldName: String) => {
      const field = fieldName.toString();
      const value: any = row[field];
      if (typeof (value) == "object") {
        row[field] = value.map((id: any) => {
          return itemMap.get(id);
        });
      } else if (typeof (value) == "string") {
        row[field] = itemMap.get(value);
      }
    });
    rows[i] = row;
  }
  res["rows"] = rows;
  console.log(res);
  return res;
}

export function setupTables() {
  (window as any)["tableResponseHandler"] = tableResponseHandler;
}
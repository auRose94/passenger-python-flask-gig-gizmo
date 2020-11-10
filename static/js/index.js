/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	function webpackJsonpCallback(data) {
/******/ 		var chunkIds = data[0];
/******/ 		var moreModules = data[1];
/******/ 		var executeModules = data[2];
/******/
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, resolves = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(Object.prototype.hasOwnProperty.call(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 				resolves.push(installedChunks[chunkId][0]);
/******/ 			}
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(data);
/******/
/******/ 		while(resolves.length) {
/******/ 			resolves.shift()();
/******/ 		}
/******/
/******/ 		// add entry modules from loaded chunk to deferred list
/******/ 		deferredModules.push.apply(deferredModules, executeModules || []);
/******/
/******/ 		// run deferred modules when all chunks ready
/******/ 		return checkDeferredModules();
/******/ 	};
/******/ 	function checkDeferredModules() {
/******/ 		var result;
/******/ 		for(var i = 0; i < deferredModules.length; i++) {
/******/ 			var deferredModule = deferredModules[i];
/******/ 			var fulfilled = true;
/******/ 			for(var j = 1; j < deferredModule.length; j++) {
/******/ 				var depId = deferredModule[j];
/******/ 				if(installedChunks[depId] !== 0) fulfilled = false;
/******/ 			}
/******/ 			if(fulfilled) {
/******/ 				deferredModules.splice(i--, 1);
/******/ 				result = __webpack_require__(__webpack_require__.s = deferredModule[0]);
/******/ 			}
/******/ 		}
/******/
/******/ 		return result;
/******/ 	}
/******/
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// object to store loaded and loading chunks
/******/ 	// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 	// Promise = chunk loading, 0 = chunk loaded
/******/ 	var installedChunks = {
/******/ 		"index": 0
/******/ 	};
/******/
/******/ 	var deferredModules = [];
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/ 	var jsonpArray = window["webpackJsonp"] = window["webpackJsonp"] || [];
/******/ 	var oldJsonpFunction = jsonpArray.push.bind(jsonpArray);
/******/ 	jsonpArray.push = webpackJsonpCallback;
/******/ 	jsonpArray = jsonpArray.slice();
/******/ 	for(var i = 0; i < jsonpArray.length; i++) webpackJsonpCallback(jsonpArray[i]);
/******/ 	var parentJsonpFunction = oldJsonpFunction;
/******/
/******/
/******/ 	// add entry module to deferred list
/******/ 	deferredModules.push(["./frontend/index.ts","vendors"]);
/******/ 	// run deferred modules when ready
/******/ 	return checkDeferredModules();
/******/ })
/************************************************************************/
/******/ ({

/***/ "./frontend/background.scss":
/*!**********************************!*\
  !*** ./frontend/background.scss ***!
  \**********************************/
/*! exports provided: default */
/*! all exports used */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _node_modules_css_loader_dist_cjs_js_node_modules_postcss_loader_dist_cjs_js_ref_5_2_node_modules_sass_loader_dist_cjs_js_background_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/css-loader/dist/cjs.js!../node_modules/postcss-loader/dist/cjs.js??ref--5-2!../node_modules/sass-loader/dist/cjs.js!./background.scss */ \"./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js?!./node_modules/sass-loader/dist/cjs.js!./frontend/background.scss\");\n\n            \n\nvar options = {};\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_node_modules_postcss_loader_dist_cjs_js_ref_5_2_node_modules_sass_loader_dist_cjs_js_background_scss__WEBPACK_IMPORTED_MODULE_1__[/* default */ \"a\"], options);\n\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (_node_modules_css_loader_dist_cjs_js_node_modules_postcss_loader_dist_cjs_js_ref_5_2_node_modules_sass_loader_dist_cjs_js_background_scss__WEBPACK_IMPORTED_MODULE_1__[/* default */ \"a\"].locals || {});\n\n//# sourceURL=webpack:///./frontend/background.scss?");

/***/ }),

/***/ "./frontend/background.ts":
/*!********************************!*\
  !*** ./frontend/background.ts ***!
  \********************************/
/*! no static exports found */
/*! all exports used */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\nvar __importDefault = (this && this.__importDefault) || function (mod) {\n    return (mod && mod.__esModule) ? mod : { \"default\": mod };\n};\nObject.defineProperty(exports, \"__esModule\", { value: true });\nexports.setupBackground = void 0;\nvar jquery_1 = __importDefault(__webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\"));\n__webpack_require__(/*! ./background.scss */ \"./frontend/background.scss\");\nvar bgSlideStart = \"bg-slide-start\";\nvar bgSlideShow = \"bg-slide-show\";\nvar storageKey = \"currentBackground\";\nfunction removeClass(className, key, toggle) {\n    if (toggle === void 0) { toggle = false; }\n    if (!toggle)\n        return className.replace(key, \"\").trim();\n    return ((className.indexOf(key) != -1) ?\n        className.replace(key, \"\") :\n        className + \" \" + key).trim();\n}\nfunction toggleBackground(element) {\n    element.className = removeClass(element.className, bgSlideShow, true);\n    element.className = removeClass(element.className, bgSlideStart);\n}\nfunction setupBackground() {\n    var backgrounds = jquery_1.default(\".bg-slide\").toArray();\n    if (Array.isArray(backgrounds)) {\n        var currentIndex = Number.parseInt(localStorage.getItem(storageKey) || \"0\");\n        var current = backgrounds[currentIndex];\n        toggleBackground(current);\n        current.className += \" \" + bgSlideStart;\n        setInterval(function () {\n            current = backgrounds[currentIndex];\n            toggleBackground(current);\n            currentIndex = (currentIndex + 1 < backgrounds.length) ? currentIndex + 1 : 0;\n            localStorage.setItem(storageKey, String(currentIndex));\n            toggleBackground(backgrounds[currentIndex]);\n        }, 10000);\n    }\n}\nexports.setupBackground = setupBackground;\n//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiYmFja2dyb3VuZC5qcyIsInNvdXJjZVJvb3QiOiIuL2Zyb250ZW5kLyIsInNvdXJjZXMiOlsiYmFja2dyb3VuZC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7QUFBQSxrREFBc0M7QUFDdEMsNkJBQTJCO0FBRTNCLElBQU0sWUFBWSxHQUFHLGdCQUFnQixDQUFDO0FBQ3RDLElBQU0sV0FBVyxHQUFHLGVBQWUsQ0FBQztBQUNwQyxJQUFNLFVBQVUsR0FBRyxtQkFBbUIsQ0FBQztBQUV2QyxTQUFTLFdBQVcsQ0FBQyxTQUFpQixFQUFFLEdBQVcsRUFBRSxNQUF1QjtJQUF2Qix1QkFBQSxFQUFBLGNBQXVCO0lBQzFFLElBQUksQ0FBQyxNQUFNO1FBQ1QsT0FBTyxTQUFTLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRSxFQUFFLENBQUMsQ0FBQyxJQUFJLEVBQUUsQ0FBQztJQUUzQyxPQUFPLENBQUMsQ0FBQyxTQUFTLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUN0QyxTQUFTLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRSxFQUFFLENBQUMsQ0FBQyxDQUFDO1FBQzVCLFNBQVMsR0FBRyxHQUFHLEdBQUcsR0FBRyxDQUFDLENBQUMsSUFBSSxFQUFFLENBQUM7QUFDbEMsQ0FBQztBQUVELFNBQVMsZ0JBQWdCLENBQUMsT0FBb0I7SUFFNUMsT0FBTyxDQUFDLFNBQVMsR0FBRyxXQUFXLENBQUMsT0FBTyxDQUFDLFNBQVMsRUFBRSxXQUFXLEVBQUUsSUFBSSxDQUFDLENBQUM7SUFDdEUsT0FBTyxDQUFDLFNBQVMsR0FBRyxXQUFXLENBQUMsT0FBTyxDQUFDLFNBQVMsRUFBRSxZQUFZLENBQUMsQ0FBQztBQUNuRSxDQUFDO0FBRUQsU0FBZ0IsZUFBZTtJQUM3QixJQUFJLFdBQVcsR0FBRyxnQkFBQyxDQUFDLFdBQVcsQ0FBQyxDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQzNDLElBQUksS0FBSyxDQUFDLE9BQU8sQ0FBQyxXQUFXLENBQUMsRUFBRTtRQUM5QixJQUFJLFlBQVksR0FBRyxNQUFNLENBQUMsUUFBUSxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsVUFBVSxDQUFDLElBQUksR0FBRyxDQUFDLENBQUM7UUFDNUUsSUFBSSxPQUFPLEdBQUcsV0FBVyxDQUFDLFlBQVksQ0FBQyxDQUFDO1FBQ3hDLGdCQUFnQixDQUFDLE9BQU8sQ0FBQyxDQUFDO1FBQzFCLE9BQU8sQ0FBQyxTQUFTLElBQUksR0FBRyxHQUFHLFlBQVksQ0FBQztRQUN4QyxXQUFXLENBQUM7WUFDVixPQUFPLEdBQUcsV0FBVyxDQUFDLFlBQVksQ0FBQyxDQUFDO1lBQ3BDLGdCQUFnQixDQUFDLE9BQU8sQ0FBQyxDQUFDO1lBQzFCLFlBQVksR0FBRyxDQUFDLFlBQVksR0FBRyxDQUFDLEdBQUcsV0FBVyxDQUFDLE1BQU0sQ0FBQyxDQUFDLENBQUMsQ0FBQyxZQUFZLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7WUFDOUUsWUFBWSxDQUFDLE9BQU8sQ0FBQyxVQUFVLEVBQUUsTUFBTSxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUM7WUFDdkQsZ0JBQWdCLENBQUMsV0FBVyxDQUFDLFlBQVksQ0FBQyxDQUFDLENBQUM7UUFDOUMsQ0FBQyxFQUFFLEtBQUssQ0FBQyxDQUFDO0tBQ1g7QUFDSCxDQUFDO0FBZkQsMENBZUMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgeyBkZWZhdWx0IGFzICQgfSBmcm9tIFwianF1ZXJ5XCI7XG5pbXBvcnQgXCIuL2JhY2tncm91bmQuc2Nzc1wiO1xuXG5jb25zdCBiZ1NsaWRlU3RhcnQgPSBcImJnLXNsaWRlLXN0YXJ0XCI7XG5jb25zdCBiZ1NsaWRlU2hvdyA9IFwiYmctc2xpZGUtc2hvd1wiO1xuY29uc3Qgc3RvcmFnZUtleSA9IFwiY3VycmVudEJhY2tncm91bmRcIjtcblxuZnVuY3Rpb24gcmVtb3ZlQ2xhc3MoY2xhc3NOYW1lOiBzdHJpbmcsIGtleTogc3RyaW5nLCB0b2dnbGU6IGJvb2xlYW4gPSBmYWxzZSk6IHN0cmluZyB7XG4gIGlmICghdG9nZ2xlKSAvLyByZW1vdmVcbiAgICByZXR1cm4gY2xhc3NOYW1lLnJlcGxhY2Uoa2V5LCBcIlwiKS50cmltKCk7IC8vIGdvbmVcbiAgLy8gdG9nZ2xlLCBlbmNhcHN1bGF0ZWQgdHJpbVxuICByZXR1cm4gKChjbGFzc05hbWUuaW5kZXhPZihrZXkpICE9IC0xKSA/IC8vIGNoZWNrIGlmIGtleSBpbiBjbGFzc25hbWVcbiAgICBjbGFzc05hbWUucmVwbGFjZShrZXksIFwiXCIpIDogLy8gcmVtb3ZlXG4gICAgY2xhc3NOYW1lICsgXCIgXCIgKyBrZXkpLnRyaW0oKTsgLy8gYWRkXG59XG5cbmZ1bmN0aW9uIHRvZ2dsZUJhY2tncm91bmQoZWxlbWVudDogSFRNTEVsZW1lbnQpIHtcbiAgLy9DaGFuZ2VzIGJhY2tncm91bmQgdG8gaW5kZXhcbiAgZWxlbWVudC5jbGFzc05hbWUgPSByZW1vdmVDbGFzcyhlbGVtZW50LmNsYXNzTmFtZSwgYmdTbGlkZVNob3csIHRydWUpO1xuICBlbGVtZW50LmNsYXNzTmFtZSA9IHJlbW92ZUNsYXNzKGVsZW1lbnQuY2xhc3NOYW1lLCBiZ1NsaWRlU3RhcnQpO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc2V0dXBCYWNrZ3JvdW5kKCkge1xuICB2YXIgYmFja2dyb3VuZHMgPSAkKFwiLmJnLXNsaWRlXCIpLnRvQXJyYXkoKTtcbiAgaWYgKEFycmF5LmlzQXJyYXkoYmFja2dyb3VuZHMpKSB7XG4gICAgdmFyIGN1cnJlbnRJbmRleCA9IE51bWJlci5wYXJzZUludChsb2NhbFN0b3JhZ2UuZ2V0SXRlbShzdG9yYWdlS2V5KSB8fCBcIjBcIik7XG4gICAgdmFyIGN1cnJlbnQgPSBiYWNrZ3JvdW5kc1tjdXJyZW50SW5kZXhdO1xuICAgIHRvZ2dsZUJhY2tncm91bmQoY3VycmVudCk7XG4gICAgY3VycmVudC5jbGFzc05hbWUgKz0gXCIgXCIgKyBiZ1NsaWRlU3RhcnQ7XG4gICAgc2V0SW50ZXJ2YWwoZnVuY3Rpb24gKCkge1xuICAgICAgY3VycmVudCA9IGJhY2tncm91bmRzW2N1cnJlbnRJbmRleF07XG4gICAgICB0b2dnbGVCYWNrZ3JvdW5kKGN1cnJlbnQpO1xuICAgICAgY3VycmVudEluZGV4ID0gKGN1cnJlbnRJbmRleCArIDEgPCBiYWNrZ3JvdW5kcy5sZW5ndGgpID8gY3VycmVudEluZGV4ICsgMSA6IDA7XG4gICAgICBsb2NhbFN0b3JhZ2Uuc2V0SXRlbShzdG9yYWdlS2V5LCBTdHJpbmcoY3VycmVudEluZGV4KSk7XG4gICAgICB0b2dnbGVCYWNrZ3JvdW5kKGJhY2tncm91bmRzW2N1cnJlbnRJbmRleF0pO1xuICAgIH0sIDEwMDAwKTtcbiAgfVxufSJdfQ==\n\n//# sourceURL=webpack:///./frontend/background.ts?");

/***/ }),

/***/ "./frontend/index.ts":
/*!***************************!*\
  !*** ./frontend/index.ts ***!
  \***************************/
/*! no static exports found */
/*! all exports used */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\nvar __importDefault = (this && this.__importDefault) || function (mod) {\n    return (mod && mod.__esModule) ? mod : { \"default\": mod };\n};\nObject.defineProperty(exports, \"__esModule\", { value: true });\n__webpack_require__(/*! bootstrap/scss/bootstrap.scss */ \"./node_modules/bootstrap/scss/bootstrap.scss\");\n__webpack_require__(/*! ./style.scss */ \"./frontend/style.scss\");\n__webpack_require__(/*! @fortawesome/fontawesome-free/scss/fontawesome.scss */ \"./node_modules/@fortawesome/fontawesome-free/scss/fontawesome.scss\");\n__webpack_require__(/*! @fortawesome/fontawesome-free/scss/regular.scss */ \"./node_modules/@fortawesome/fontawesome-free/scss/regular.scss\");\n__webpack_require__(/*! @fortawesome/fontawesome-free/scss/solid.scss */ \"./node_modules/@fortawesome/fontawesome-free/scss/solid.scss\");\n__webpack_require__(/*! @fortawesome/fontawesome-free/scss/v4-shims.scss */ \"./node_modules/@fortawesome/fontawesome-free/scss/v4-shims.scss\");\n__webpack_require__(/*! bootstrap */ \"./node_modules/bootstrap/dist/js/bootstrap.js\");\n__webpack_require__(/*! popper.js */ \"./node_modules/popper.js/dist/esm/popper.js\");\nvar background_1 = __webpack_require__(/*! ./background */ \"./frontend/background.ts\");\nvar jquery_1 = __importDefault(__webpack_require__(/*! jquery */ \"./node_modules/jquery/dist/jquery.js\"));\nvar table_1 = __webpack_require__(/*! ./table */ \"./frontend/table.ts\");\njquery_1.default(function () {\n    background_1.setupBackground();\n    table_1.setupTables();\n});\n//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiaW5kZXguanMiLCJzb3VyY2VSb290IjoiLi9mcm9udGVuZC8iLCJzb3VyY2VzIjpbImluZGV4LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7O0FBQUEseUNBQXVDO0FBQ3ZDLHdCQUFzQjtBQUN0QiwrREFBNEQ7QUFDNUQsMkRBQXdEO0FBQ3hELHlEQUFzRDtBQUN0RCw0REFBeUQ7QUFDekQscUJBQW1CO0FBQ25CLHFCQUFtQjtBQUNuQiwyQ0FBK0M7QUFDL0Msa0RBQXNDO0FBQ3RDLGlDQUFzQztBQUV0QyxnQkFBQyxDQUFDO0lBRUEsNEJBQWUsRUFBRSxDQUFDO0lBQ2xCLG1CQUFXLEVBQUUsQ0FBQztBQUNoQixDQUFDLENBQUMsQ0FBQyIsInNvdXJjZXNDb250ZW50IjpbImltcG9ydCBcImJvb3RzdHJhcC9zY3NzL2Jvb3RzdHJhcC5zY3NzXCI7XG5pbXBvcnQgXCIuL3N0eWxlLnNjc3NcIjtcbmltcG9ydCBcIkBmb3J0YXdlc29tZS9mb250YXdlc29tZS1mcmVlL3Njc3MvZm9udGF3ZXNvbWUuc2Nzc1wiXG5pbXBvcnQgXCJAZm9ydGF3ZXNvbWUvZm9udGF3ZXNvbWUtZnJlZS9zY3NzL3JlZ3VsYXIuc2Nzc1wiXG5pbXBvcnQgXCJAZm9ydGF3ZXNvbWUvZm9udGF3ZXNvbWUtZnJlZS9zY3NzL3NvbGlkLnNjc3NcIlxuaW1wb3J0IFwiQGZvcnRhd2Vzb21lL2ZvbnRhd2Vzb21lLWZyZWUvc2Nzcy92NC1zaGltcy5zY3NzXCJcbmltcG9ydCBcImJvb3RzdHJhcFwiO1xuaW1wb3J0IFwicG9wcGVyLmpzXCI7XG5pbXBvcnQgeyBzZXR1cEJhY2tncm91bmQgfSBmcm9tIFwiLi9iYWNrZ3JvdW5kXCI7XG5pbXBvcnQgeyBkZWZhdWx0IGFzICQgfSBmcm9tIFwianF1ZXJ5XCI7XG5pbXBvcnQgeyBzZXR1cFRhYmxlcyB9IGZyb20gXCIuL3RhYmxlXCI7XG5cbiQoZnVuY3Rpb24gKCkge1xuICAvLyBET00gcmVhZHksIHRha2UgaXQgYXdheVxuICBzZXR1cEJhY2tncm91bmQoKTtcbiAgc2V0dXBUYWJsZXMoKTtcbn0pOyJdfQ==\n\n//# sourceURL=webpack:///./frontend/index.ts?");

/***/ }),

/***/ "./frontend/style.scss":
/*!*****************************!*\
  !*** ./frontend/style.scss ***!
  \*****************************/
/*! exports provided: default */
/*! all exports used */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ \"./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js\");\n/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);\n/* harmony import */ var _node_modules_css_loader_dist_cjs_js_node_modules_postcss_loader_dist_cjs_js_ref_5_2_node_modules_sass_loader_dist_cjs_js_style_scss__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/css-loader/dist/cjs.js!../node_modules/postcss-loader/dist/cjs.js??ref--5-2!../node_modules/sass-loader/dist/cjs.js!./style.scss */ \"./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js?!./node_modules/sass-loader/dist/cjs.js!./frontend/style.scss\");\n\n            \n\nvar options = {};\n\noptions.insert = \"head\";\noptions.singleton = false;\n\nvar update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_node_modules_postcss_loader_dist_cjs_js_ref_5_2_node_modules_sass_loader_dist_cjs_js_style_scss__WEBPACK_IMPORTED_MODULE_1__[/* default */ \"a\"], options);\n\n\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (_node_modules_css_loader_dist_cjs_js_node_modules_postcss_loader_dist_cjs_js_ref_5_2_node_modules_sass_loader_dist_cjs_js_style_scss__WEBPACK_IMPORTED_MODULE_1__[/* default */ \"a\"].locals || {});\n\n//# sourceURL=webpack:///./frontend/style.scss?");

/***/ }),

/***/ "./frontend/table.ts":
/*!***************************!*\
  !*** ./frontend/table.ts ***!
  \***************************/
/*! no static exports found */
/*! all exports used */
/***/ (function(module, exports, __webpack_require__) {

"use strict";
eval("\nObject.defineProperty(exports, \"__esModule\", { value: true });\nexports.setupTables = void 0;\n__webpack_require__(/*! bootstrap-table/src/bootstrap-table.scss */ \"./node_modules/bootstrap-table/src/bootstrap-table.scss\");\n__webpack_require__(/*! bootstrap-table */ \"./node_modules/bootstrap-table/dist/bootstrap-table.min.js\");\nvar luxon_1 = __webpack_require__(/*! luxon */ \"./node_modules/luxon/build/cjs-browser/luxon.js\");\nfunction parseElapsedDate(row, field) {\n    if (typeof (row[field]) == \"number\") {\n        var then = luxon_1.DateTime.fromSeconds(Math.floor(row[field]));\n        row[field] = then.toRelative();\n    }\n}\nfunction parseModel(row) {\n    parseElapsedDate(row, \"created\");\n    parseElapsedDate(row, \"updated\");\n    return row;\n}\nfunction tableResponseHandler(res) {\n    var rows = res.rows;\n    var maps = new Map();\n    var allowed = [\"rows\", \"total\"];\n    var _loop_1 = function (key) {\n        if (Object.prototype.hasOwnProperty.call(res, key)) {\n            var value_1 = res[key];\n            if (allowed.indexOf(key) == -1) {\n                var itemMap = new Map(Object.keys(value_1).map(function (id) {\n                    return [id, parseModel(value_1[id])];\n                }));\n                maps.set(key, itemMap);\n            }\n        }\n    };\n    for (var key in res) {\n        _loop_1(key);\n    }\n    var _loop_2 = function (i) {\n        var row = parseModel(rows[i]);\n        maps.forEach(function (itemMap, fieldName) {\n            var field = fieldName.toString();\n            var value = row[field];\n            if (typeof (value) == \"object\") {\n                row[field] = value.map(function (id) {\n                    return itemMap.get(id);\n                });\n            }\n            else if (typeof (value) == \"string\") {\n                row[field] = itemMap.get(value);\n            }\n        });\n        rows[i] = row;\n    };\n    for (var i = 0; i < rows.length; i++) {\n        _loop_2(i);\n    }\n    res[\"rows\"] = rows;\n    console.log(res);\n    return res;\n}\nfunction setupTables() {\n    window[\"tableResponseHandler\"] = tableResponseHandler;\n}\nexports.setupTables = setupTables;\n//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoidGFibGUuanMiLCJzb3VyY2VSb290IjoiLi9mcm9udGVuZC8iLCJzb3VyY2VzIjpbInRhYmxlLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7OztBQUNBLG9EQUFrRDtBQUNsRCwyQkFBeUI7QUFDekIsK0JBQWtEO0FBU2xELFNBQVMsZ0JBQWdCLENBQUMsR0FBbUIsRUFBRSxLQUFhO0lBQzFELElBQUksT0FBTSxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsQ0FBQyxJQUFJLFFBQVEsRUFBRTtRQUNsQyxJQUFJLElBQUksR0FBRyxnQkFBUSxDQUFDLFdBQVcsQ0FBQyxJQUFJLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUM7UUFDeEQsR0FBRyxDQUFDLEtBQUssQ0FBQyxHQUFHLElBQUksQ0FBQyxVQUFVLEVBQUUsQ0FBQztLQUNoQztBQUNILENBQUM7QUFFRCxTQUFTLFVBQVUsQ0FBQyxHQUFtQjtJQUNyQyxnQkFBZ0IsQ0FBQyxHQUFHLEVBQUUsU0FBUyxDQUFDLENBQUM7SUFDakMsZ0JBQWdCLENBQUMsR0FBRyxFQUFFLFNBQVMsQ0FBQyxDQUFDO0lBQ2pDLE9BQU8sR0FBRyxDQUFDO0FBQ2IsQ0FBQztBQUVELFNBQVMsb0JBQW9CLENBQUMsR0FBUTtJQUNwQyxJQUFJLElBQUksR0FBSSxHQUFHLENBQUMsSUFBOEIsQ0FBQztJQUMvQyxJQUFJLElBQUksR0FBRyxJQUFJLEdBQUcsRUFBdUMsQ0FBQztJQUMxRCxJQUFJLE9BQU8sR0FBRyxDQUFDLE1BQU0sRUFBRSxPQUFPLENBQUMsQ0FBQzs0QkFFckIsR0FBRztRQUNaLElBQUksTUFBTSxDQUFDLFNBQVMsQ0FBQyxjQUFjLENBQUMsSUFBSSxDQUFDLEdBQUcsRUFBRSxHQUFHLENBQUMsRUFBRTtZQUNsRCxJQUFNLE9BQUssR0FBRyxHQUFHLENBQUMsR0FBRyxDQUFDLENBQUM7WUFDdkIsSUFBSSxPQUFPLENBQUMsT0FBTyxDQUFDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBQyxFQUFFO2dCQUM5QixJQUFJLE9BQU8sR0FBRyxJQUFJLEdBQUcsQ0FBeUIsTUFBTSxDQUFDLElBQUksQ0FBQyxPQUFLLENBQUMsQ0FBQyxHQUFHLENBQUMsVUFBQyxFQUFFO29CQUN0RSxPQUFPLENBQUMsRUFBRSxFQUFFLFVBQVUsQ0FBQyxPQUFLLENBQUMsRUFBRSxDQUFDLENBQUMsQ0FBQyxDQUFDO2dCQUNyQyxDQUFDLENBQUMsQ0FBQyxDQUFDO2dCQUNKLElBQUksQ0FBQyxHQUFHLENBQUMsR0FBRyxFQUFFLE9BQU8sQ0FBQyxDQUFDO2FBQ3hCO1NBQ0Y7O0lBVEgsS0FBSyxJQUFNLEdBQUcsSUFBSSxHQUFHO2dCQUFWLEdBQUc7S0FVYjs0QkFDUSxDQUFDO1FBQ1IsSUFBTSxHQUFHLEdBQUcsVUFBVSxDQUFDLElBQUksQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDO1FBQ2hDLElBQUksQ0FBQyxPQUFPLENBQUMsVUFBQyxPQUFPLEVBQUUsU0FBaUI7WUFDdEMsSUFBTSxLQUFLLEdBQUcsU0FBUyxDQUFDLFFBQVEsRUFBRSxDQUFDO1lBQ25DLElBQU0sS0FBSyxHQUFRLEdBQUcsQ0FBQyxLQUFLLENBQUMsQ0FBQztZQUM5QixJQUFJLE9BQU8sQ0FBQyxLQUFLLENBQUMsSUFBSSxRQUFRLEVBQUU7Z0JBQzlCLEdBQUcsQ0FBQyxLQUFLLENBQUMsR0FBRyxLQUFLLENBQUMsR0FBRyxDQUFDLFVBQUMsRUFBTztvQkFDN0IsT0FBTyxPQUFPLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyxDQUFDO2dCQUN6QixDQUFDLENBQUMsQ0FBQzthQUNKO2lCQUFNLElBQUksT0FBTyxDQUFDLEtBQUssQ0FBQyxJQUFJLFFBQVEsRUFBRTtnQkFDckMsR0FBRyxDQUFDLEtBQUssQ0FBQyxHQUFHLE9BQU8sQ0FBQyxHQUFHLENBQUMsS0FBSyxDQUFDLENBQUM7YUFDakM7UUFDSCxDQUFDLENBQUMsQ0FBQztRQUNILElBQUksQ0FBQyxDQUFDLENBQUMsR0FBRyxHQUFHLENBQUM7O0lBYmhCLEtBQUssSUFBSSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsR0FBRyxJQUFJLENBQUMsTUFBTSxFQUFFLENBQUMsRUFBRTtnQkFBM0IsQ0FBQztLQWNUO0lBQ0QsR0FBRyxDQUFDLE1BQU0sQ0FBQyxHQUFHLElBQUksQ0FBQztJQUNuQixPQUFPLENBQUMsR0FBRyxDQUFDLEdBQUcsQ0FBQyxDQUFDO0lBQ2pCLE9BQU8sR0FBRyxDQUFDO0FBQ2IsQ0FBQztBQUVELFNBQWdCLFdBQVc7SUFDeEIsTUFBYyxDQUFDLHNCQUFzQixDQUFDLEdBQUcsb0JBQW9CLENBQUM7QUFDakUsQ0FBQztBQUZELGtDQUVDIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IHsgZGVmYXVsdCBhcyAkLCB0eXBlIH0gZnJvbSBcImpxdWVyeVwiO1xuaW1wb3J0IFwiYm9vdHN0cmFwLXRhYmxlL3NyYy9ib290c3RyYXAtdGFibGUuc2Nzc1wiO1xuaW1wb3J0IFwiYm9vdHN0cmFwLXRhYmxlXCI7XG5pbXBvcnQgbHV4b24sIHsgRGF0ZVRpbWUsIEludGVydmFsIH0gZnJvbSBcImx1eG9uXCI7IFxuXG5pbnRlcmZhY2UgTW9kZWxJbnRlcmZhY2Uge1xuICBfaWQ6IHN0cmluZztcbiAgY3JlYXRlZDogbnVtYmVyIHwgc3RyaW5nO1xuICB1cGRhdGVkOiBudW1iZXIgfCBzdHJpbmc7XG4gIFtmaWVsZDogc3RyaW5nXTogYW55O1xufVxuXG5mdW5jdGlvbiBwYXJzZUVsYXBzZWREYXRlKHJvdzogTW9kZWxJbnRlcmZhY2UsIGZpZWxkOiBzdHJpbmcpIHtcbiAgaWYgKHR5cGVvZihyb3dbZmllbGRdKSA9PSBcIm51bWJlclwiKSB7XG4gICAgbGV0IHRoZW4gPSBEYXRlVGltZS5mcm9tU2Vjb25kcyhNYXRoLmZsb29yKHJvd1tmaWVsZF0pKTtcbiAgICByb3dbZmllbGRdID0gdGhlbi50b1JlbGF0aXZlKCk7XG4gIH1cbn1cblxuZnVuY3Rpb24gcGFyc2VNb2RlbChyb3c6IE1vZGVsSW50ZXJmYWNlKSB7XG4gIHBhcnNlRWxhcHNlZERhdGUocm93LCBcImNyZWF0ZWRcIik7XG4gIHBhcnNlRWxhcHNlZERhdGUocm93LCBcInVwZGF0ZWRcIik7XG4gIHJldHVybiByb3c7XG59XG5cbmZ1bmN0aW9uIHRhYmxlUmVzcG9uc2VIYW5kbGVyKHJlczogYW55KTogYW55IHtcbiAgbGV0IHJvd3MgPSAocmVzLnJvd3MgYXMgQXJyYXk8TW9kZWxJbnRlcmZhY2U+KTtcbiAgbGV0IG1hcHMgPSBuZXcgTWFwPFN0cmluZywgTWFwPFN0cmluZywgTW9kZWxJbnRlcmZhY2U+PigpO1xuICBsZXQgYWxsb3dlZCA9IFtcInJvd3NcIiwgXCJ0b3RhbFwiXTtcbiAgXG4gIGZvciAoY29uc3Qga2V5IGluIHJlcykge1xuICAgIGlmIChPYmplY3QucHJvdG90eXBlLmhhc093blByb3BlcnR5LmNhbGwocmVzLCBrZXkpKSB7XG4gICAgICBjb25zdCB2YWx1ZSA9IHJlc1trZXldO1xuICAgICAgaWYgKGFsbG93ZWQuaW5kZXhPZihrZXkpID09IC0xKSB7XG4gICAgICAgIGxldCBpdGVtTWFwID0gbmV3IE1hcDxTdHJpbmcsIE1vZGVsSW50ZXJmYWNlPihPYmplY3Qua2V5cyh2YWx1ZSkubWFwKChpZCkgPT4ge1xuICAgICAgICAgIHJldHVybiBbaWQsIHBhcnNlTW9kZWwodmFsdWVbaWRdKV07XG4gICAgICAgIH0pKTtcbiAgICAgICAgbWFwcy5zZXQoa2V5LCBpdGVtTWFwKTtcbiAgICAgIH1cbiAgICB9XG4gIH1cbiAgZm9yIChsZXQgaSA9IDA7IGkgPCByb3dzLmxlbmd0aDsgaSsrKSB7XG4gICAgY29uc3Qgcm93ID0gcGFyc2VNb2RlbChyb3dzW2ldKTtcbiAgICBtYXBzLmZvckVhY2goKGl0ZW1NYXAsIGZpZWxkTmFtZTogU3RyaW5nKSA9PiB7XG4gICAgICBjb25zdCBmaWVsZCA9IGZpZWxkTmFtZS50b1N0cmluZygpO1xuICAgICAgY29uc3QgdmFsdWU6IGFueSA9IHJvd1tmaWVsZF07XG4gICAgICBpZiAodHlwZW9mICh2YWx1ZSkgPT0gXCJvYmplY3RcIikge1xuICAgICAgICByb3dbZmllbGRdID0gdmFsdWUubWFwKChpZDogYW55KSA9PiB7XG4gICAgICAgICAgcmV0dXJuIGl0ZW1NYXAuZ2V0KGlkKTtcbiAgICAgICAgfSk7XG4gICAgICB9IGVsc2UgaWYgKHR5cGVvZiAodmFsdWUpID09IFwic3RyaW5nXCIpIHtcbiAgICAgICAgcm93W2ZpZWxkXSA9IGl0ZW1NYXAuZ2V0KHZhbHVlKTtcbiAgICAgIH1cbiAgICB9KTtcbiAgICByb3dzW2ldID0gcm93O1xuICB9XG4gIHJlc1tcInJvd3NcIl0gPSByb3dzO1xuICBjb25zb2xlLmxvZyhyZXMpO1xuICByZXR1cm4gcmVzO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gc2V0dXBUYWJsZXMoKSB7XG4gICh3aW5kb3cgYXMgYW55KVtcInRhYmxlUmVzcG9uc2VIYW5kbGVyXCJdID0gdGFibGVSZXNwb25zZUhhbmRsZXI7XG59Il19\n\n//# sourceURL=webpack:///./frontend/table.ts?");

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js?!./node_modules/sass-loader/dist/cjs.js!./frontend/background.scss":
/*!*******************************************************************************************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js??ref--5-2!./node_modules/sass-loader/dist/cjs.js!./frontend/background.scss ***!
  \*******************************************************************************************************************************************************************/
/*! exports provided: default */
/*! exports used: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ \"./node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.i, \".bg-slide-start {\\n  transition: none !important;\\n  z-index: -999 !important;\\n  opacity: 1 !important;\\n}\\n\\n.bg-slide {\\n  position: fixed;\\n  top: 0;\\n  left: 0;\\n  width: 100%;\\n  height: 100%;\\n  background-size: cover;\\n  background-repeat: no-repeat;\\n  background-position: center;\\n  z-index: -1000;\\n  opacity: 0;\\n  transition: opacity 0.5s ease;\\n}\\n\\n.bg-slide-show {\\n  z-index: -999 !important;\\n  opacity: 1 !important;\\n}\\n\\n#bg {\\n  position: fixed;\\n  top: 0;\\n  left: 0;\\n  width: 100%;\\n  height: 100%;\\n  background-size: cover;\\n  background-repeat: no-repeat;\\n  background-position: center;\\n  z-index: -1000;\\n  background-color: #444444;\\n}\", \"\"]);\n// Exports\n/* harmony default export */ __webpack_exports__[\"a\"] = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack:///./frontend/background.scss?./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js??ref--5-2!./node_modules/sass-loader/dist/cjs.js");

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js?!./node_modules/sass-loader/dist/cjs.js!./frontend/style.scss":
/*!**************************************************************************************************************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js??ref--5-2!./node_modules/sass-loader/dist/cjs.js!./frontend/style.scss ***!
  \**************************************************************************************************************************************************************/
/*! exports provided: default */
/*! exports used: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ \"./node_modules/css-loader/dist/runtime/api.js\");\n/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0__);\n// Imports\n\nvar ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_0___default()(function(i){return i[1]});\n// Module\n___CSS_LOADER_EXPORT___.push([module.i, \".content {\\n  width: auto;\\n  margin: 5em 10em 5em 10em;\\n}\\n\\n@media screen and (max-width: 1000px) {\\n  .content {\\n    width: auto;\\n    margin: 5em 0 10em 0;\\n  }\\n}\", \"\"]);\n// Exports\n/* harmony default export */ __webpack_exports__[\"a\"] = (___CSS_LOADER_EXPORT___);\n\n\n//# sourceURL=webpack:///./frontend/style.scss?./node_modules/css-loader/dist/cjs.js!./node_modules/postcss-loader/dist/cjs.js??ref--5-2!./node_modules/sass-loader/dist/cjs.js");

/***/ })

/******/ });
import { default as $ } from "jquery";
import "./background.scss";

const bgSlideStart = "bg-slide-start";
const bgSlideShow = "bg-slide-show";
const storageKey = "currentBackground";

function removeClass(className: string, key: string, toggle: boolean = false): string {
  if (!toggle) // remove
    return className.replace(key, "").trim(); // gone
  // toggle, encapsulated trim
  return ((className.indexOf(key) != -1) ? // check if key in classname
    className.replace(key, "") : // remove
    className + " " + key).trim(); // add
}

function toggleBackground(element: HTMLElement) {
  //Changes background to index
  element.className = removeClass(element.className, bgSlideShow, true);
  element.className = removeClass(element.className, bgSlideStart);
}

export function setupBackground() {
  var backgrounds = $(".bg-slide").toArray();
  if (Array.isArray(backgrounds)) {
    var currentIndex = Number.parseInt(localStorage.getItem(storageKey) || "0");
    var current = backgrounds[currentIndex];
    toggleBackground(current);
    current.className += " " + bgSlideStart;
    setInterval(function () {
      current = backgrounds[currentIndex];
      toggleBackground(current);
      currentIndex = (currentIndex + 1 < backgrounds.length) ? currentIndex + 1 : 0;
      localStorage.setItem(storageKey, String(currentIndex));
      toggleBackground(backgrounds[currentIndex]);
    }, 10000);
  }
}
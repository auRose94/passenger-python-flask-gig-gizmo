import "bootstrap/scss/bootstrap.scss";
import "./style.scss";
import "@fortawesome/fontawesome-free/scss/fontawesome.scss"
import "@fortawesome/fontawesome-free/scss/regular.scss"
import "@fortawesome/fontawesome-free/scss/solid.scss"
import "@fortawesome/fontawesome-free/scss/v4-shims.scss"
import "bootstrap";
import "popper.js";
import { setupBackground } from "./background";
import { default as $ } from "jquery";
import { setupTables } from "./table";

$(function () {
  // DOM ready, take it away
  setupBackground();
  setupTables();
});
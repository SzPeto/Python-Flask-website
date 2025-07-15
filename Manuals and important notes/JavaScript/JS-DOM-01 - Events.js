/* This is the preferred and modern way of communicating with html trough event listeners
   We can pass data into html lines with data-name - it will be called as : dataset.name */

const testScripts = document.querySelectorAll(".base-h-box-blog");
for(let i = 0; i < testScripts.length; i++) {
    testScripts[i].addEventListener("click", () => {
        alert(testScripts[i].dataset.post);
    });
}

/* This is the less preferred way of communicating with html, you can use onclick, onsubmit etc. inside
   html tags, like : <div onclick="testFunction('It is working!')"></div> */
   
function testFunction(text) {
    alert(text);
}

/* 
===========================
 Common DOM Event Types
===========================

🖱 Mouse Events:
----------------
- "click"        → Element is clicked
- "dblclick"     → Element is double-clicked
- "mousedown"    → Mouse button is pressed down
- "mouseup"      → Mouse button is released
- "mouseenter"   → Mouse enters the element
- "mouseleave"   → Mouse leaves the element
- "mousemove"    → Mouse is moved over the element
- "contextmenu"  → Right-click on the element

⌨️ Keyboard Events:
-------------------
- "keydown"      → Key is pressed
- "keyup"        → Key is released
- "keypress"     → (deprecated) Key is pressed

📝 Form & Input Events:
------------------------
- "submit"       → A form is submitted
- "input"        → Input field changes (in real time)
- "change"       → Field loses focus after change
- "focus"        → Input field gains focus
- "blur"         → Input field loses focus
- "reset"        → Form is reset

📄 Document & Window Events:
-----------------------------
- "load"         → Page or resource finishes loading
- "DOMContentLoaded" → HTML has been fully parsed
- "resize"       → Browser window is resized
- "scroll"       → User scrolls the page or element
- "unload"       → User leaves the page (deprecated in modern browsers)

*/
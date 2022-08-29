// function to change window title
var title;
window.onblur = function() {
    title = document.title;
    document.title = "Leaving page";
};
window.onfocus = function() {
    if (title) {
        document.title = title;
    }
}
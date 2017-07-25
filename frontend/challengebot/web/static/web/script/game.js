$(document).ready(function() {
    var elem = document.getElementById("id_your_code");
    var editor = CodeMirror.fromTextArea(elem, {mode: "text/x-python", lineNumbers: true, theme: "material", tabSize: 4, indentUnit: 4, matchBrackets: true});
    editor.setSize("100%", "500px");
    function setLanguage() {
        if ($("#id_language option:selected").val() == "PY2" || $("#id_language option:selected").val() == "PY3") {
            editor.setOption("mode", "text/x-python");
            editor.getDoc().setValue($("#python-code").text());
        }
        if ($("#id_language option:selected").val() == "Cpp") {
            editor.setOption("mode", "text/x-c++src");
            editor.getDoc().setValue($("#cpp-code").text());
        }
    }
    $("#id_language").change(setLanguage);
    setLanguage();
});
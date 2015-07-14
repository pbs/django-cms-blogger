function showEntryPreviewPopup(triggeringLink, admin_static_url) {
    var win = window.open('', 'EntryPreview', 'height=800,width=1024,resizable=yes,scrollbars=yes');
    if(win) {
        html = '';
        html += '<div class="loading"></div>';
        html += '<style>';
        html += '.loading {';
        html += 'width: 100%; height: 100%;';
        html += 'background: url(\"' + admin_static_url + 'img/spinner.gif\") center center no-repeat;}';
        html += '</style>';
        win.document.open();
        win.document.write(html);
        win.document.close();
    }

    function getEditorHtmlContent(){
        if (window.tinyMCE !== undefined){
            return tinyMCE.activeEditor.getContent();
        }
        var editors = (window.CKEDITOR || {'instances': []}).instances
        for (var ed in editors) {
            return editors[ed].getData();
        }
        return "No editor content available."
    }

    $.ajax({
        type: "POST",
        datatype: "text",
        url: triggeringLink.href,
        data: { "body": getEditorHtmlContent() },
        success: function(data) {
            win.document.open();
            win.document.write(data);
            win.document.close();
        }
    });
}

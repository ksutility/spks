var TabManager = {
    tabKey: 9, // This number means tab key ascii input.
    enableTab: function(textBox, keyEvent) {
        if(this.isTabKeyInput(keyEvent)) {
            // Put tab key into the current cursor(caret) position.
            this.insertTab(textBox);
            
            // Block(invalidate) actual tab key input by returning key event handler to false.
            this.blockKeyEvent(keyEvent);   
        }
    },
    isTabKeyInput: function(keyEvent) {
        return keyEvent.keyCode == this.tabKey; 
    },
    insertTab: function(textBox) {
        var pos = this.getCaretPosition(textBox);
        var preText = textBox.value.substring(0, pos);
        var postText = textBox.value.substring(pos, textBox.value.length);

        textBox.value = preText + "\t" + postText; // input tab key

        this.setCaretPosition(textBox, pos + 1);
    },
    setCaretPosition: function(item, pos) {
        // Firefox, Chrome, IE9~ Support
        if(item.setSelectionRange) {
            item.focus();
            item.setSelectionRange(pos, pos);
        }
        // ~IE9 Support
        else if (item.createTextRange) {
            var range = item.createTextRange();
            range.collapse(true);
            range.moveEnd('character', pos);
            range.moveStart('character', pos);
            range.select();
        }
    },
    getCaretPosition: function(item) {
        var caretPosition = 0;
        
        // Firefox, Chrome, IE9~ Support
        if(item.selectionStart || item.selectionStart == '0') {
            caretPosition = item.selectionStart;
        }
        // ~IE9 Support
        else if(document.selection) {
            item.focus();
            var sel = document.selection.createRange();
            sel.moveStart('character', -item.value.length);
            caretPosition = sel.text.length;
        }
        
        return caretPosition;
    },
    blockKeyEvent: function(keyEvent) {
        if(keyEvent.preventDefault) {
            keyEvent.preventDefault();
        }
        else {
            keyEvent.returnValue = false;
        }
    }
};
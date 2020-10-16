$(document).ready(function(){
    //======================================
    //======= range slider activate ========
    //======================================
    var power = $('#power');
    var diskspace = $('#diskspace');
    var ram = $('#ram');
    var brandwidth = $('#brandwidth');
    
    $('#rgslider').slider({
        range: "min",
        value: 20,
        step: 20,
        slide: function (event, ui) {
            if (20 == ui.value) {
                power.text('02');
                diskspace.text('100');
                ram.text('04');
                brandwidth.text('3000');
            } else if (40 == ui.value) {
                power.text('04');
                diskspace.text('200');
                ram.text('06');
                brandwidth.text('4000');
            } else if (60 == ui.value) {
                power.text('06');
                diskspace.text('300');
                ram.text('08');
                brandwidth.text('5000');

            } else if (80 == ui.value) {
                power.text('08');
                diskspace.text('400');
                ram.text('08');
                brandwidth.text('6000');
            } else {
                power.text('10');
                diskspace.text('500');
                ram.text('10');
                brandwidth.text('7000');
            }
        }
    });
});
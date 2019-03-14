"use strict";

$.fn.mdbAutocomplete = function (options) {
  var defaults = {
    data: {},
    dataColor: '',
    xColor: '',
    xBlurColor: '#ced4da',
    inputFocus: '1px solid #4285f4',
    inputBlur: '1px solid #ced4da',
    inputFocusShadow: '0 1px 0 0 #4285f4',
    inputBlurShadow: ''
  };
  var ENTER_CHAR_CODE = 13;
  options = $.extend(defaults, options);
  return this.each(function (index, ev) {
    var $input = $(ev);
    var $autocomplete;
    var data = options.data;
    var dataColor = options.dataColor;
    var xColor = options.xColor;
    var xBlurColor = options.xBlurColor;
    var inputFocus = options.inputFocus;
    var inputBlur = options.inputBlur;
    var inputFocusShadow = options.inputFocusShadow;
    var inputBlurShadow = options.inputBlurShadow;

    if (Object.keys(data).length) {
      $autocomplete = $('<ul class="mdb-autocomplete-wrap"></ul>');
      $autocomplete.insertAfter($input);
    }

    $input.on('focus', function () {
      $input.css('border-bottom', inputFocus);
      $input.css('box-shadow', inputFocusShadow);
    });
    $input.on('blur', function () {
      $input.css('border-bottom', inputBlur);
      $input.css('box-shadow', inputBlurShadow);
    });
    $input.on('keyup', function (e) {
      var $inputValue = $input.val();
      $autocomplete.empty();

      if ($inputValue.length) {
        for (var item in data) {
          if (data[item].toLowerCase().indexOf($inputValue.toLowerCase()) !== -1) {
            var option = $("<li>".concat(data[item], "</li>"));
            $autocomplete.append(option);
          }
        }
      }

      if (e.which === ENTER_CHAR_CODE) {
        $autocomplete.children(':first').trigger('click');
        $autocomplete.empty();
      }

      if ($inputValue.length === 0) {
        $input.parent().find('.mdb-autocomplete-clear').css('visibility', 'hidden');
      } else {
        $input.parent().find('.mdb-autocomplete-clear').css('visibility', 'visible');
      }

      $('.mdb-autocomplete-wrap li').css('color', dataColor);
    });
    $autocomplete.on('click', 'li', function (e) {
      $input.val($(e.target).text());
      $autocomplete.empty();
    });
    $('.mdb-autocomplete-clear').on('click', function (e) {
      e.preventDefault();
      var $this = $(e.currentTarget);
      $this.parent().find('.mdb-autocomplete').val('');
      $this.css('visibility', 'hidden');
      $autocomplete.empty();
      $this.parent().find('label').removeClass('active');
    });
    $('.mdb-autocomplete').on('click keyup', function (e) {
      e.preventDefault();
      $(e.target).parent().find('.mdb-autocomplete-clear').find('svg').css('fill', xColor);
    });
    $('.mdb-autocomplete').on('blur', function (e) {
      e.preventDefault();
      $(e.target).parent().find('.mdb-autocomplete-clear').find('svg').css('fill', xBlurColor);
    });
  });
};

$.fn.mdb_autocomplete = $.fn.mdbAutocomplete;
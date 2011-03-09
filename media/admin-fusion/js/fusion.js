

// cookie functions
jQuery.cookie = function(name, value, options) {
    if (typeof value != 'undefined') { // name and value given, set cookie
        options = options || {};
        if (value === null) {
            value = '';
            options = jQuery.extend({}, options); // clone object since it's unexpected behavior if the expired property were changed
            options.expires = -1;
        }
        var expires = '';
        if (options.expires && (typeof options.expires == 'number' || options.expires.toUTCString)) {
            var date;
            if (typeof options.expires == 'number') {
                date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
            } else {
                date = options.expires;
            }
            expires = '; expires=' + date.toUTCString(); // use expires attribute, max-age is not supported by IE
        }
        // NOTE Needed to parenthesize options.path and options.domain
        // in the following expressions, otherwise they evaluate to undefined
        // in the packed version for some reason...
        var path = options.path ? '; path=' + (options.path) : '';
        var domain = options.domain ? '; domain=' + (options.domain) : '';
        var secure = options.secure ? '; secure' : '';
        document.cookie = [name, '=', encodeURIComponent(value), expires, path, domain, secure].join('');
    } else { // only name given, get cookie
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
};
// /cookie functions

// fixes for IE-7 cleartype bug on fade in/out
jQuery.fn.fadeIn = function(speed, callback) {
 return this.animate({opacity: 'show'}, speed, function() {
  if (jQuery.browser.msie) this.style.removeAttribute('filter');
  if (jQuery.isFunction(callback)) callback();
 });
};

jQuery.fn.fadeOut = function(speed, callback) {
 return this.animate({opacity: 'hide'}, speed, function() {
  if (jQuery.browser.msie) this.style.removeAttribute('filter');
  if (jQuery.isFunction(callback)) callback();
 });
};

jQuery.fn.fadeTo = function(speed,to,callback) {
 return this.animate({opacity: to}, speed, function() {
  if (to == 1 && jQuery.browser.msie) this.style.removeAttribute('filter');
  if (jQuery.isFunction(callback)) callback();
 });
};


// liquid <> fixed
function setPageWidth(){
   var currentWidth = jQuery('#page').css('width');
   if (currentWidth=="95%") newWidth = "960px"; else if (currentWidth=="960px") newWidth = "95%"; else newWidth = "960px";
   jQuery("#page").animate({width: newWidth}, 333).fadeIn("slow");
   jQuery.cookie('pageWidth', newWidth);
}

// body font size
function setFontSize() {
   var size = jQuery.cookie('fontSize');
   if (size=='.8em') newSize = '.95em';
   else if (size=='.95em') newSize = '.7em';
   else if (size=='.7em') newSize = '.8em';
   else newSize = '.95em';
   jQuery("body").animate({fontSize: newSize}, 333).fadeIn("slow");
   jQuery.cookie('fontSize',newSize)
}

// minitabs
jQuery.fn.minitabs = function(speed,effect) {
  id = "#" + this.attr('id')
  jQuery(id + ">DIV:gt(0)").hide();
  jQuery(id + ">UL>LI>A:first").addClass("current");
  jQuery(id + ">UL>LI>A").click(
    function(){
      jQuery(id + ">UL>LI>A").removeClass("current");
      jQuery(this).addClass("current");
      jQuery(this).blur();
      var re = /([_\-\w]+$)/i;
      var target = jQuery('#' + re.exec(this.href)[1]);
      var old = jQuery(id + ">DIV");
      switch (effect) {
        case 'fade':
          old.fadeOut(speed).fadeOut(speed);
          target.fadeIn(speed);
          break;
        case 'slide':
          old.slideUp(speed);
          target.fadeOut(speed).fadeIn(speed);
          break;
        default :
          old.hide(speed);
          target.show(speed)
      }
      return false;
    }
 );
}

function initTooltips(o) {
  var showTip = function() {
  	var el = jQuery('.tip', this).css('display', 'block')[0];
  	var ttHeight = jQuery(el).height();
    var ttOffset =  el.offsetHeight;
	var ttTop = ttOffset + ttHeight;
    jQuery('.tip', this)
	  .stop()
	  .css({'opacity': 0, 'top': 2 - ttOffset})
  	  .animate({'opacity': 1, 'top': 18 - ttOffset}, 250);
	};
	var hideTip = function() {
  	  var self = this;
	  var el = jQuery('.tip', this).css('display', 'block')[0];
      var ttHeight = jQuery(el).height();
	  var ttOffset =  el.offsetHeight;
	  var ttTop = ttOffset + ttHeight;
      jQuery('.tip', this)
	  	.stop()
	  	.animate({'opacity': 0,'top': 10 - ttOffset}, 250, function() {
		   el.hiding = false;
		   jQuery(this).css('display', 'none');
		}
      );
	};
	jQuery('.tip').hover(
	  function() { return false; },
	  function() { return true; }
	);
	jQuery('.tiptrigger, #sidebar .cat-item').hover(
	  function(){
	  	var self = this;
	  	showTip.apply(this);
	  	if (o.timeout) this.tttimeout = setTimeout(function() { hideTip.apply(self) } , o.timeout);
	  },
	  function() {
	  	clearTimeout(this.tttimeout);
	  	hideTip.apply(this);
	  }
	);
}

function tabmenudropdowns(){
jQuery(" #tabs ul ul ").css({display: "none"}); // Opera Fix
jQuery(" #tabs li").hover(function(){
  jQuery(this).find('ul:first').css({visibility: "visible",display: "none"}).show(333);
 },function(){
    jQuery(this).find('ul:first').css({visibility: "hidden"});
   });
}


jQuery(document).ready(function(){
      // body .safari class
      if (jQuery.browser.safari) jQuery('body').addClass('safari');

      // layout controls
       jQuery("#layoutcontrol a").click(function() {
         switch (jQuery(this).attr("class")) {
    	   case 'setFont' : setFontSize();	break;
    	   case 'setLiquid'	: setPageWidth();	break;
    	 }
    	 return false;
        });
       // set the font size from cookie
       var font_size = jQuery.cookie('fontSize');
       if (font_size == '.7em') { jQuery('body').css("font-size",".7em"); }
       if (font_size == '.95em') { jQuery('body').css("font-size",".95em"); }
       if (font_size == '.8em') { jQuery('body').css("font-size",".8em"); }

       // set the page width from cookie
       var page_width = jQuery.cookie('pageWidth');
       if (page_width) jQuery('#page').css('width', page_width);

      jQuery('#secondary-tabs').minitabs(333, 'slide');

      if (document.all && !window.opera && !window.XMLHttpRequest && jQuery.browser.msie) { var isIE6 = true; }
      else { var isIE6 = false;} ;
      jQuery.browser.msie6 = isIE6;
      if (!isIE6) {
        initTooltips({
    		timeout: 6000
       });
      }
      tabmenudropdowns();

      // some jquery effects...
      jQuery('#sidebar ul.nav li ul li a').mouseover(function () {
       	jQuery(this).animate({ marginLeft: "4px" }, 100 );
      });
      jQuery('#sidebar ul.nav li ul li a').mouseout(function () {
        jQuery(this).animate({ marginLeft: "0px" }, 100 );
      });
      // scroll to top
      jQuery("a#toplink").click(function(){
        jQuery('html, body').animate({scrollTop:0}, 'slow');
      });

});
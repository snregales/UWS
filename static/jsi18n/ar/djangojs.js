

(function(globals) {

  var django = globals.django || (globals.django = {});

  
  django.pluralidx = function(n) {
    var v=n==0 ? 0 : n==1 ? 1 : n==2 ? 2 : n%100>=3 && n%100<=10 ? 3 : n%100>=11 && n%100<=99 ? 4 : 5;
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  var newcatalog = {
    "%(sel)s of %(cnt)s selected": [
      "\u0644\u0627 \u0634\u064a \u0645\u062d\u062f\u062f",
      "%(sel)s \u0645\u0646 %(cnt)s \u0645\u062d\u062f\u062f",
      "%(sel)s \u0645\u0646 %(cnt)s \u0645\u062d\u062f\u062f",
      "%(sel)s \u0645\u0646 %(cnt)s \u0645\u062d\u062f\u062f\u0629",
      "%(sel)s \u0645\u0646 %(cnt)s \u0645\u062d\u062f\u062f",
      "%(sel)s \u0645\u0646 %(cnt)s \u0645\u062d\u062f\u062f"
    ],
    "6 a.m.": "6 \u0635.",
    "6 p.m.": "6 \u0645\u0633\u0627\u0621\u064b",
    "Available %s": "%s \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629",
    "Cancel": "\u0623\u0644\u063a",
    "Choose": "\u0627\u062e\u062a\u064a\u0627\u0631",
    "Choose a Date": "\u0625\u062e\u062a\u0631 \u062a\u0627\u0631\u064a\u062e ",
    "Choose a Time": "\u0625\u062e\u062a\u0631 \u0648\u0642\u062a",
    "Choose a time": "\u0627\u062e\u062a\u0631 \u0648\u0642\u062a\u0627\u064b",
    "Choose all": "\u0627\u062e\u062a\u0631 \u0627\u0644\u0643\u0644",
    "Chosen %s": "%s \u0627\u0644\u0645\u064f\u062e\u062a\u0627\u0631\u0629",
    "Click to choose all %s at once.": "\u0627\u0636\u063a\u0637 \u0644\u0627\u062e\u062a\u064a\u0627\u0631 \u062c\u0645\u064a\u0639 %s \u062c\u0645\u0644\u0629 \u0648\u0627\u062d\u062f\u0629.",
    "Click to remove all chosen %s at once.": "\u0627\u0636\u063a\u0637 \u0644\u0625\u0632\u0627\u0644\u0629 \u062c\u0645\u064a\u0639 %s \u0627\u0644\u0645\u062d\u062f\u062f\u0629 \u062c\u0645\u0644\u0629 \u0648\u0627\u062d\u062f\u0629.",
    "Filter": "\u0627\u0646\u062a\u0642\u0627\u0621",
    "Hide": "\u0627\u062e\u0641",
    "Midnight": "\u0645\u0646\u062a\u0635\u0641 \u0627\u0644\u0644\u064a\u0644",
    "Noon": "\u0627\u0644\u0638\u0647\u0631",
    "Note: You are %s hour ahead of server time.": [
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645."
    ],
    "Note: You are %s hour behind server time.": [
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645."
    ],
    "Now": "\u0627\u0644\u0622\u0646",
    "Remove": "\u0627\u062d\u0630\u0641",
    "Remove all": "\u0625\u0632\u0627\u0644\u0629 \u0627\u0644\u0643\u0644",
    "Show": "\u0623\u0638\u0647\u0631",
    "This is the list of available %s. You may choose some by selecting them in the box below and then clicking the \"Choose\" arrow between the two boxes.": "\u0647\u0630\u0647 \u0642\u0627\u0626\u0645\u0629 %s \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629. \u064a\u0645\u0643\u0646\u0643 \u0627\u062e\u062a\u064a\u0627\u0631 \u0628\u0639\u0636\u0647\u0627 \u0628\u0627\u0646\u062a\u0642\u0627\u0626\u0647\u0627 \u0641\u064a \u0627\u0644\u0635\u0646\u062f\u0648\u0642 \u0623\u062f\u0646\u0627\u0647 \u062b\u0645 \u0627\u0644\u0636\u063a\u0637 \u0639\u0644\u0649 \u0633\u0647\u0645 \u0627\u0644\u0640\"\u0627\u062e\u062a\u064a\u0627\u0631\" \u0628\u064a\u0646 \u0627\u0644\u0635\u0646\u062f\u0648\u0642\u064a\u0646.",
    "This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the \"Remove\" arrow between the two boxes.": "\u0647\u0630\u0647 \u0642\u0627\u0626\u0645\u0629 %s \u0627\u0644\u0645\u062d\u062f\u062f\u0629. \u064a\u0645\u0643\u0646\u0643 \u0625\u0632\u0627\u0644\u0629 \u0628\u0639\u0636\u0647\u0627 \u0628\u0627\u062e\u062a\u064a\u0627\u0631\u0647\u0627 \u0641\u064a \u0627\u0644\u0635\u0646\u062f\u0648\u0642 \u0623\u062f\u0646\u0627\u0647 \u062b\u0645 \u0627\u0636\u063a\u0637 \u0639\u0644\u0649 \u0633\u0647\u0645 \u0627\u0644\u0640\"\u0625\u0632\u0627\u0644\u0629\" \u0628\u064a\u0646 \u0627\u0644\u0635\u0646\u062f\u0648\u0642\u064a\u0646.",
    "Today": "\u0627\u0644\u064a\u0648\u0645",
    "Tomorrow": "\u063a\u062f\u0627\u064b",
    "Type into this box to filter down the list of available %s.": "\u0627\u0643\u062a\u0628 \u0641\u064a \u0647\u0630\u0627 \u0627\u0644\u0635\u0646\u062f\u0648\u0642 \u0644\u062a\u0635\u0641\u064a\u0629 \u0642\u0627\u0626\u0645\u0629 %s \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629.",
    "Yesterday": "\u0623\u0645\u0633",
    "You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button.": "\u0627\u062e\u062a\u0631\u062a \u0625\u062c\u0631\u0627\u0621\u064b \u062f\u0648\u0646 \u062a\u063a\u064a\u064a\u0631 \u0623\u064a \u062d\u0642\u0644. \u0644\u0639\u0644\u0643 \u062a\u0631\u064a\u062f \u0632\u0631 \u0627\u0644\u062a\u0646\u0641\u064a\u0630 \u0628\u062f\u0644\u0627\u064b \u0645\u0646 \u0632\u0631 \u0627\u0644\u062d\u0641\u0638.",
    "You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action.": "\u0627\u062e\u062a\u0631\u062a \u0625\u062c\u0631\u0627\u0621\u064b \u0644\u0643\u0646 \u062f\u0648\u0646 \u0623\u0646 \u062a\u062d\u0641\u0638 \u062a\u063a\u064a\u064a\u0631\u0627\u062a \u0627\u0644\u062a\u064a \u0642\u0645\u062a \u0628\u0647\u0627. \u0631\u062c\u0627\u0621 \u0627\u0636\u063a\u0637 \u0632\u0631 \u0627\u0644\u0645\u0648\u0627\u0641\u0642\u0629 \u0644\u062a\u062d\u0641\u0638 \u062a\u0639\u062f\u064a\u0644\u0627\u062a\u0643. \u0633\u062a\u062d\u062a\u0627\u062c \u0625\u0644\u0649 \u0625\u0639\u0627\u062f\u0629 \u062a\u0646\u0641\u064a\u0630 \u0627\u0644\u0625\u062c\u0631\u0627\u0621.",
    "You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.": "\u0644\u062f\u064a\u0643 \u062a\u0639\u062f\u064a\u0644\u0627\u062a \u063a\u064a\u0631 \u0645\u062d\u0641\u0648\u0638\u0629 \u0639\u0644\u0649 \u0628\u0639\u0636 \u0627\u0644\u062d\u0642\u0648\u0644 \u0627\u0644\u0642\u0627\u0628\u0644\u0629 \u0644\u0644\u062a\u0639\u062f\u064a\u0644. \u0625\u0646 \u0646\u0641\u0630\u062a \u0623\u064a \u0625\u062c\u0631\u0627\u0621 \u0641\u0633\u0648\u0641 \u062a\u062e\u0633\u0631 \u062a\u0639\u062f\u064a\u0644\u0627\u062a\u0643."
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value[django.pluralidx(count)];
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P",
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d",
      "%m/%d/%Y %H:%M:%S",
      "%m/%d/%Y %H:%M:%S.%f",
      "%m/%d/%Y %H:%M",
      "%m/%d/%Y",
      "%m/%d/%y %H:%M:%S",
      "%m/%d/%y %H:%M:%S.%f",
      "%m/%d/%y %H:%M",
      "%m/%d/%y"
    ],
    "DATE_FORMAT": "j F\u060c Y",
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d",
      "%m/%d/%Y",
      "%m/%d/%y",
      "%b %d %Y",
      "%b %d, %Y",
      "%d %b %Y",
      "%d %b, %Y",
      "%B %d %Y",
      "%B %d, %Y",
      "%d %B %Y",
      "%d %B, %Y"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 0,
    "MONTH_DAY_FORMAT": "j F",
    "NUMBER_GROUPING": 0,
    "SHORT_DATETIME_FORMAT": "m/d/Y P",
    "SHORT_DATE_FORMAT": "d\u200f/m\u200f/Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "g:i A",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));


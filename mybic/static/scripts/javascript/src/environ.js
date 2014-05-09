define(['jquery', 'underscore', 'backbone', 'core/mixins', 'bootstrap'], function($, _, Backbone, Mixins) {
  var ATTEMPTS, App, CSRF_TOKEN, MAX_ATTEMPTS, SCRIPT_NAME, absolutePath, safeMethod, sameOrigin, _ajax;
  this.App = App = this.App || {};
  App.Models = {};
  App.Views = {};
  ATTEMPTS = 0;
  MAX_ATTEMPTS = 3;
  _.templateSettings = {
    evaluate: /\{\{\#\s*([^\s]+?)\s*\}\}/g,
    interpolate: /\{\{\s*([^\s]+?)\s*\}\}/g,
    escape: /\{\{\-\s*([^\s]+?)\s*\}\}/g
  };
  if ((SCRIPT_NAME = this.SCRIPT_NAME) === void 0) {
    throw Error('Global "SCRIPT_NAME" not defined');
  }
  if ((CSRF_TOKEN = this.CSRF_TOKEN) === void 0) {
    throw Error('Global "CSRF_TOKEN" not defined');
  }
  sameOrigin = function(url) {
    var host, origin, protocol, sr_origin;
    host = document.location.host;
    protocol = document.location.protocol;
    sr_origin = '//' + host;
    origin = protocol + sr_origin;
    return (url === origin || url.slice(0, origin.length + 1) === origin + '/') || (url === sr_origin || url.slice(0, sr_origin.length + 1) === sr_origin + '/') || !(/^(\/\/|http:|https:).*/.test(url));
  };
  safeMethod = function(method) {
    return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
  };
  absolutePath = function(path) {
    return SCRIPT_NAME + path;
  };
  $.ajaxPrefilter(function(settings, origSettings, xhr) {
    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
      return xhr.setRequestHeader('X-CSRFToken', CSRF_TOKEN);
    }
  });
  $(window).on('beforeunload', function() {
    if (Backbone.ajax.pending) {
      if (ATTEMPTS === MAX_ATTEMPTS) {
        return "Unfortunately, your data hasn't been saved. The server                    or your Internet connection is acting up. Sorry!";
      }
      return "Wow, you're quick! Your stuff is being saved.                It will only take a moment.";
    }
  });
  _.extend(Backbone.View.prototype, Mixins.Deferrable);
  _.extend(Backbone.Model.prototype, Mixins.Deferrable);
  _.extend(Backbone.Collection.prototype, Mixins.Deferrable);
  _.extend(Backbone.Router.prototype, Mixins.Deferrable);
  _ajax = Backbone.ajax;
  Backbone.ajax = function(options) {
    return this.ajax.queue(options);
  };
  Backbone.ajax.pending = false;
  Backbone.ajax.requests = [];
  Backbone.ajax.requestNext = function() {
    var args, options, promise;
    if ((args = this.requests.shift())) {
      options = args[0], promise = args[1];
      return this.request(options, promise);
    } else {
      return this.pending = false;
    }
  };
  Backbone.ajax.request = function(_options, promise, trigger) {
    var complete, error, options, params, success,
      _this = this;
    if (trigger == null) {
      trigger = true;
    }
    options = _.extend({}, _options);
    success = options.success;
    error = options.error;
    complete = options.complete;
    params = {
      complete: function(xhr, status) {
        var _ref;
        if (status === 'timeout') {
          if (ATTEMPTS < MAX_ATTEMPTS) {
            return _ajax(params);
          }
        } else if ((200 <= (_ref = xhr.status) && _ref < 300)) {
          if (complete) {
            complete.apply(_this, arguments);
          }
          if (trigger) {
            return _this.requestNext();
          }
        } else {
          return _this.pending = false;
        }
      },
      success: function() {
        if (success) {
          success.apply(this, arguments);
        }
        return promise.resolveWith(this, arguments);
      },
      error: function(xhr, status, err) {
        if (status === 'timeout' && ATTEMPTS < MAX_ATTEMPTS) {
          return ATTEMPTS++;
        } else {
          if (error) {
            error.apply(this, arguments);
          }
          return promise.rejectWith(this, arguments);
        }
      }
    };
    params = _.extend(options, params);
    _ajax(params);
    return ATTEMPTS = 1;
  };
  Backbone.ajax.queue = function(options) {
    var promise, type;
    type = (options.type || 'get').toLowerCase();
    promise = $.Deferred();
    if (type === 'get') {
      this.request(options, promise, false);
    } else if (this.pending) {
      this.requests.push([options, promise]);
    } else {
      this.pending = true;
      this.request(options, promise);
    }
    return promise;
  };
  return {
    CSRF_TOKEN: CSRF_TOKEN,
    SCRIPT_NAME: SCRIPT_NAME,
    absolutePath: absolutePath
  };
});

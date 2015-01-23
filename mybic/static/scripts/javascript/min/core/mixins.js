define(['jquery', 'underscore'], function($, _) {
  var Deferrable;
  Deferrable = {
    deferred: {},
    initialize: function() {
      var method, once, _fn, _ref,
        _this = this;
      this.pending();
      _ref = this.deferred;
      _fn = function(method, once) {
        var func;
        func = _this[method];
        return _this[method] = function() {
          return _this.defer(method, func, once, arguments);
        };
      };
      for (method in _ref) {
        once = _ref[method];
        _fn(method, once);
      }
    },
    pending: function() {
      (this._deferred = $.Deferred()).once = {};
      return this;
    },
    defer: function(name, func, once, args) {
      if (once == null) {
        once = false;
      }
      if (this._deferred == null) {
        this.pending();
      }
      if (_.isString(name)) {
        if (_.isBoolean(func)) {
          once = func;
          func = this[name];
        }
        if (once) {
          if (this._deferred[name]) {
            return this;
          }
          this._deferred.once[name] = true;
        }
      } else {
        func = name;
      }
      this._deferred.done(function() {
        return func.apply(null, args);
      });
      return this;
    },
    resolve: function(context) {
      if (context == null) {
        context = this;
      }
      if (this._deferred) {
        this._deferred.resolveWith(context);
      }
      return this;
    },
    reject: function(context) {
      if (context == null) {
        context = this;
      }
      if (this._deferred) {
        this._deferred.rejectWith(context);
      }
      return this;
    },
    promise: function() {
      var _ref;
      if (this._deferred == null) {
        this.pending();
      }
      return (_ref = this._deferred).promise.apply(_ref, arguments);
    },
    when: function(func) {
      return $.when(this).done(func);
    },
    state: function() {
      var _ref;
      return (_ref = this._deferred) != null ? _ref.state() : void 0;
    }
  };
  Deferrable.resolveWith = Deferrable.resolve;
  Deferrable.rejectWith = Deferrable.reject;
  return {
    Deferrable: Deferrable
  };
});

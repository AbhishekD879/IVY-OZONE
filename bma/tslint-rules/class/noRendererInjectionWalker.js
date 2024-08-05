"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
exports.__esModule = true;
var Lint = require("tslint");
var NoRendererInjectionWalker = /** @class */ (function (_super) {
    __extends(NoRendererInjectionWalker, _super);
    function NoRendererInjectionWalker() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * visitConstructorDeclaration()
     * @param {ts.ConstructorDeclaration} node
     */
    NoRendererInjectionWalker.prototype.visitConstructorDeclaration = function (node) {
        var _this = this;
        node.parameters.forEach(function (param) {
            var token = param.type && param.type.getText();
            if (token && token === 'Renderer2') {
                _this.addFailureAtNode(node, NoRendererInjectionWalker.FAILURE_STRING, NoRendererInjectionWalker.fix(node));
            }
        });
        _super.prototype.visitConstructorDeclaration.call(this, node);
    };
    /**
     * fix()
     * @param {ts.ConstructorDeclaration} node
     * @returns {Lint.Fix}
     */
    NoRendererInjectionWalker.fix = function (node) {
        return new Lint.Replacement(node.pos, node.end, '');
    };
    NoRendererInjectionWalker.FAILURE_STRING = 'Injection of Renderer2 is forbidden. Use RendererService instead.';
    return NoRendererInjectionWalker;
}(Lint.RuleWalker));
exports.NoRendererInjectionWalker = NoRendererInjectionWalker;

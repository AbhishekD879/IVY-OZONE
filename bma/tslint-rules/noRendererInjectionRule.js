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
var noRendererInjectionWalker_1 = require("./class/noRendererInjectionWalker");
/**
 * @description Compile: tsc tslint-rules/noRendererInjectionRule.ts --lib "es2015, dom"
 */
var Rule = /** @class */ (function (_super) {
    __extends(Rule, _super);
    function Rule() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * apply()
     * @param { ts.SourceFile } sourceFile
     * @returns { Lint.RuleFailure[] }
     */
    Rule.prototype.apply = function (sourceFile) {
        return this.applyWithWalker(new noRendererInjectionWalker_1.NoRendererInjectionWalker(sourceFile, this.getOptions()));
    };
    Rule.metadata = {
        ruleName: 'no-renderer-injection',
        type: 'maintainability',
        description: "Ensures that 'RendererService' is used instead of 'Renderer2'.",
        options: null,
        optionsDescription: 'Not configurable',
        rationale: "Injection of 'Renderer2' in services will cause an error.",
        typescriptOnly: true
    };
    return Rule;
}(Lint.Rules.AbstractRule));
exports.Rule = Rule;

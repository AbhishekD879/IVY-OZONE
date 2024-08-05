import * as Lint from 'tslint';
import * as ts from 'typescript';
import { NoRendererInjectionWalker } from './class/noRendererInjectionWalker';

/**
 * @description Compile: tsc tslint-rules/noRendererInjectionRule.ts --lib "es2015, dom"
 */
export class Rule extends Lint.Rules.AbstractRule {

  static readonly metadata: Lint.IRuleMetadata = {
    ruleName: 'no-renderer-injection',
    type: 'maintainability',
    description: `Ensures that 'RendererService' is used instead of 'Renderer2'.`,
    options: null,
    optionsDescription: 'Not configurable',
    rationale: `Injection of 'Renderer2' in services will cause an error.`,
    typescriptOnly: true,
  };

  /**
   * apply()
   * @param { ts.SourceFile } sourceFile
   * @returns { Lint.RuleFailure[] }
   */
  apply(sourceFile: ts.SourceFile): Lint.RuleFailure[] {
    return this.applyWithWalker(new NoRendererInjectionWalker(sourceFile, this.getOptions()));
  }
}

import * as Lint from 'tslint';
import * as ts from 'typescript';

export class NoRendererInjectionWalker extends Lint.RuleWalker {

  static readonly FAILURE_STRING = 'Injection of Renderer2 is forbidden. Use RendererService instead.';

  /**
   * visitConstructorDeclaration()
   * @param {ts.ConstructorDeclaration} node
   */
  protected visitConstructorDeclaration(node: ts.ConstructorDeclaration): void {
    node.parameters.forEach(param => {
      const token = param.type && param.type.getText();

      if (token && token === 'Renderer2') {
        this.addFailureAtNode(
          node,
          NoRendererInjectionWalker.FAILURE_STRING,
          NoRendererInjectionWalker.fix(node)
        );
      }
    });

    super.visitConstructorDeclaration(node);
  }

  /**
   * fix()
   * @param {ts.ConstructorDeclaration} node
   * @returns {Lint.Fix}
   */
  private static fix(node: ts.ConstructorDeclaration): Lint.Fix {
    return new Lint.Replacement(node.pos, node.end, '');
  }
}

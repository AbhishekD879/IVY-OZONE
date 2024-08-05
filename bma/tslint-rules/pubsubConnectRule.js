const Lint = require('tslint');
const ts = require('typescript');

class Rule extends Lint.Rules.AbstractRule {
  apply(srcFile) {
    if (!this._checkFileName(srcFile.fileName)) {
      return [];
    }

    this._findConstructor(srcFile);
    if (!this._constructor) {
      return [];
    }

    this._findServicesNames();
    if (!this._pubsubName && !this._connectName) {
      return [];
    }

    this._callExpressions = [];
    this._findCallExpressions(srcFile);

    this._subscribeMap = new Map();
    this._unsubscribeMap = new Map();
    this._syncMap = new Map();
    this._unsyncMap = new Map();
    this._callExpressions.forEach(node => this._processCallExpression(node));

    return this._getErrors(srcFile);
  }

  _checkFileName(fileName) {
    return /(component|directive|pipe)\.ts$/.test(fileName);
  }

  _findConstructor(node) {
    if (this._constructor) {
      return;
    } else if (node.kind === ts.SyntaxKind.Constructor) {
      this._constructor = node;
    } else {
      node.forEachChild(child => this._findConstructor(child));
    }
  }

  _findServicesNames() {
    this._constructor.parameters.forEach(param => {
      const type = param.type && param.type.getText();
      if (type === 'PubSubService') {
        this._pubsubName = param.name.text;
      } else if (type === 'ConnectService') {
        this._connectName = param.name.text;
      }
    });
  }

  _findCallExpressions(node) {
    if (node.kind === ts.SyntaxKind.CallExpression) {
      this._callExpressions.push(node);
    }
    node.forEachChild(child => this._findCallExpressions(child));
  }

  _processCallExpression(node) {
    const text = node.getText();

    if (this._pubsubName) {
      if (text.startsWith(`this.${this._pubsubName}.subscribe`)) {
        this._subscribeMap.set(this._getCallExpFirstParam(node), node);
      } else if (text.startsWith(`this.${this._pubsubName}.unsubscribe`)) {
        this._unsubscribeMap.set(this._getCallExpFirstParam(node), node);
      }
    }

    if (this._connectName) {
      if (text.startsWith(`this.${this._connectName}.sync`)) {
        this._syncMap.set(this._getCallExpFirstParam(node), node);
      } else if (text.startsWith(`this.${this._connectName}.unsync`)) {
        this._unsyncMap.set(this._getCallExpFirstParam(node), node);
      }
    }
  }

  _getErrors(srcFile) {
    const errors = [];

    this._subscribeMap.forEach((node, name) => {
      if (!this._unsubscribeMap.has(name)) {
        errors.push({ node, text: `cannot find "unsubscribe" call for "${name}"` });
      }
    });
    this._unsubscribeMap.forEach((node, name) => {
      if (!this._subscribeMap.has(name)) {
        errors.push({ node, text: `cannot find "subscribe" call for "${name}"` });
      }
    });

    this._syncMap.forEach((node, name) => {
      if (!this._unsyncMap.has(name)) {
        errors.push({ node, text: `cannot find "unsync" call for "${name}"` });
      }
    });
    this._unsyncMap.forEach((node, name) => {
      if (!this._syncMap.has(name)) {
        errors.push({ node, text: `cannot find "sync" call for "${name}"` });
      }
    });

    return errors.map(err => new Lint.RuleFailure(
      srcFile, err.node.getStart(), err.node.getEnd(), err.text, this.ruleName
    ));
  }

  _getCallExpFirstParam(node) {
    try {
      return node.getChildAt(2).getChildAt(0).getText();
    } catch (e) {
      return '';
    }
  }

  _printNode(node, indent = 0) {
    console.log(`${' '.repeat(indent)} ${ts.SyntaxKind[node.kind]}`);
    (node.getChildren() || []).forEach(child => this._printNode(child, indent + 2));
  }
}

module.exports.Rule = Rule;

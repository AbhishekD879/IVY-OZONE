package com.egalacoral.spark.timeform.controller.api;

@javax.annotation.Generated(
    value = "class io.swagger.codegen.languages.SpringCodegen",
    date = "2016-09-02T07:48:35.998Z")
public class NotFoundException extends ApiException {

  private static final long serialVersionUID = -1002331493666864704L;

  private int code;

  public NotFoundException(int code, String msg) {
    super(code, msg);
    this.code = code;
  }

  public int getCode() {
    return code;
  }
}

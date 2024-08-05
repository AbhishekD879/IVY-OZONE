package com.egalacoral.spark.timeform.model.internal;

import com.egalacoral.spark.timeform.model.Meeting;
import com.google.gson.annotations.SerializedName;

import java.util.Collections;
import java.util.List;

public class DataResponse<T> {

  @SerializedName("odata.error")
  private Error error;

  @SerializedName("odata.metadata")
  private String metadata;

  @SerializedName("odata.count")
  private Integer totalCount;

  @SerializedName("value")
  private List<T> entities;

  public List<T> getEntities() {
    return entities;
  }

  public String getMetadata() {
    return metadata;
  }

  public Error getError() {
    return error;
  }

  @Override
  public String toString() {
    final StringBuilder sb = new StringBuilder("DataResponse{");
    sb.append("error='").append(error).append('\'');
    sb.append("metadata='").append(metadata).append('\'');
    sb.append("totalCount='").append(totalCount).append('\'');
    if (entities != null) {
      sb.append(", entities.count=").append(entities.size());
    }
    sb.append(", entities=").append(entities);
    sb.append('}');
    return sb.toString();
  }

  public Integer getTotalCount() {
    return totalCount;
  }

  /**
   * for testing purposes only
   * */
  @Deprecated
  public void setTotalCount(Integer totalCount) {
    this.totalCount = totalCount;
  }

  /**
   * for testing purposes only
   * */
  @Deprecated
  public void setEntities(List<T> entities) {
    this.entities = entities;
  }

  public static class Error {

    @SerializedName("code")
    private String code;

    @SerializedName("message")
    private ErrorMessage message;

    public String getCode() {
      return code;
    }

    public ErrorMessage getMessage() {
      return message;
    }

    @Override
    public String toString() {
      final StringBuilder sb = new StringBuilder("Error{");
      sb.append("code='").append(code).append('\'');
      sb.append(", message='").append(message).append('\'');
      sb.append('}');
      return sb.toString();
    }
  }

  public static class ErrorMessage {

    @SerializedName("lang")
    private String lang;

    @SerializedName("value")
    private String value;

    public String getLang() {
      return lang;
    }

    public String getValue() {
      return value;
    }

    @Override
    public String toString() {
      final StringBuilder sb = new StringBuilder("ErrorMessage{");
      sb.append("lang='").append(lang).append('\'');
      sb.append(", value='").append(value).append('\'');
      sb.append('}');
      return sb.toString();
    }
  }
}

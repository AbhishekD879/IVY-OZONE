package com.egalacoral.spark.timeform.model;

import java.io.Serializable;

/**
 * This is sample class for testing cache.
 *
 * @author Vitalij Havryk
 */
public class ExampleMeeting implements Serializable {

  private static final long serialVersionUID = 1L;

  private String id;
  private String name;

  public ExampleMeeting(String id, String name) {
    this.id = id;
    this.name = name;
  }

  public String getId() {
    return id;
  }

  public void setId(String id) {
    this.id = id;
  }

  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  @Override
  public String toString() {
    return "Meeting [id=" + id + ", name=" + name + "]";
  }
}

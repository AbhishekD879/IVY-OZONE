package com.coral.oxygen.middleware.ms.quickbet.connector.dto.liveserv;

public class OutputChannel {
  private final String name;
  private final long id;
  private final String type;

  public OutputChannel(String name, long id, String type) {
    this.name = name;
    this.id = id;
    this.type = type;
  }

  public String getName() {
    return name;
  }

  public long getId() {
    return id;
  }

  public String getType() {
    return type;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof OutputChannel)) return false;

    OutputChannel that = (OutputChannel) o;

    if (getId() != that.getId()) return false;
    if (!getName().equals(that.getName())) return false;
    return getType().equals(that.getType());
  }

  @Override
  public int hashCode() {
    int result = getName().hashCode();
    result = 31 * result + (int) (getId() ^ (getId() >>> 32));
    result = 31 * result + getType().hashCode();
    return result;
  }
}

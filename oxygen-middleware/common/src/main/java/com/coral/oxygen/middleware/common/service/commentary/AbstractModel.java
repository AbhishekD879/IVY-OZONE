package com.coral.oxygen.middleware.common.service.commentary;

import java.util.Map;

/** Created by Aliaksei Yarotski on 5/16/18. */
public abstract class AbstractModel {

  private final Map<String, Object> fields;

  AbstractModel(Map<String, Object> fields) {
    this.fields = fields;
  }

  public Object getField(Object name) {
    return getField(name.toString());
  }

  public Object getField(String name) {
    return fields.get(name);
  }

  public void setField(Object name, Object value) {
    setField(name.toString(), value);
  }

  public void setField(String name, Object value) {
    fields.put(name, value);
  }

  public Map<String, Object> toMap() {
    return fields;
  }

  public boolean isEmpty() {
    return fields == null || fields.isEmpty();
  }

  public boolean equalByValues(AbstractModel another) {
    if (this.fields.size() != another.fields.size()) {
      return false;
    }
    for (Map.Entry<String, Object> entity : fields.entrySet()) {
      if (!another.fields.containsKey(entity.getKey())) {
        return false;
      }
      if (!entity.getValue().toString().equals(another.getField(entity.getKey()))) {
        return false;
      }
    }
    return true;
  }
}

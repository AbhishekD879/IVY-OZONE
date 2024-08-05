package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.storage.Storage;
import java.util.Date;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ActionCalendarStorageService {

  public static final String ACTION_CACHE_NAME = "action";

  private Storage storage;

  @Autowired
  public ActionCalendarStorageService(Storage storage) {
    this.storage = storage;
  }

  public void save(String operationName, Date date) {
    Map<String, Date> map = storage.getMap(ACTION_CACHE_NAME);
    map.put(operationName, date);
  }

  public Date getValue(String operationName) {
    Map<String, Date> map = storage.getMap(ACTION_CACHE_NAME);
    return map.get(operationName);
  }

  public Map<String, Date> getAll() {
    Map<String, Date> map = storage.getMap(ACTION_CACHE_NAME);
    return map.entrySet().stream()
        .collect(Collectors.toMap(entry -> entry.getKey(), entry -> entry.getValue()));
  }

  public void deleteKey(String key) {
    storage.getMap(ACTION_CACHE_NAME).remove(key);
  }
}

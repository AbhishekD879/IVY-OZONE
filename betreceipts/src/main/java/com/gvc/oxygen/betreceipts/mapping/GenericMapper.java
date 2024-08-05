package com.gvc.oxygen.betreceipts.mapping;

import org.modelmapper.ModelMapper;
import org.modelmapper.TypeToken;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class GenericMapper<T, V> {

  private ModelMapper modelMapper;

  @Autowired
  public GenericMapper(ModelMapper modelMapper) {
    this.modelMapper = modelMapper;
  }

  public V map(T entity, Class<V> clazz) {
    return modelMapper.map(entity, clazz);
  }

  public V mapGenericClasses(T entity, TypeToken<V> typeToken) {
    return modelMapper.map(entity, typeToken.getType());
  }
}

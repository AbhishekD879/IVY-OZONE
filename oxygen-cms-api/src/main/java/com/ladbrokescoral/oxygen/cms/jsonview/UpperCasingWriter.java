package com.ladbrokescoral.oxygen.cms.jsonview;

import com.fasterxml.jackson.core.JsonGenerator;
import com.fasterxml.jackson.databind.SerializerProvider;
import com.fasterxml.jackson.databind.ser.BeanPropertyWriter;

public class UpperCasingWriter extends BeanPropertyWriter {
  final BeanPropertyWriter writer;

  public UpperCasingWriter(final BeanPropertyWriter w) {
    super(w);
    writer = w;
  }

  @Override
  public void serializeAsField(
      final Object bean, final JsonGenerator gen, final SerializerProvider prov) throws Exception {
    String value = ((User) bean).name;
    value = (value == null) ? "" : value.toUpperCase();
    gen.writeStringField("name", value);
  }
}

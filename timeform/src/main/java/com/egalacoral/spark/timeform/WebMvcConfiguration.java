package com.egalacoral.spark.timeform;

import com.egalacoral.spark.timeform.gson.GsonUKDateAdapter;
import com.egalacoral.spark.timeform.timer.TimerService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import java.io.IOException;
import java.lang.reflect.Type;
import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpOutputMessage;
import org.springframework.http.converter.HttpMessageConverter;
import org.springframework.http.converter.HttpMessageNotWritableException;
import org.springframework.http.converter.json.GsonHttpMessageConverter;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;

/** Created by Igor.Domshchikov on 8/15/2016. */
@Configuration
public class WebMvcConfiguration extends WebMvcConfigurerAdapter {

  @Autowired private TimerService timerService;

  @Override
  public void configureMessageConverters(List<HttpMessageConverter<?>> converters) {
    GsonHttpMessageConverter msgConverter =
        new GsonHttpMessageConverter() {
          @Override
          protected void writeInternal(Object t, HttpOutputMessage outputMessage)
              throws IOException, HttpMessageNotWritableException {
            // TODO Auto-generated method stub
            super.writeInternal(t, outputMessage);
          }

          @Override
          protected void writeInternal(Object o, Type type, HttpOutputMessage outputMessage)
              throws IOException, HttpMessageNotWritableException {
            // TODO Auto-generated method stub
            super.writeInternal(o, type, outputMessage);
          }
        };

    GsonUKDateAdapter typeAdapter = new GsonUKDateAdapter();
    Gson gson =
        new GsonBuilder()
            .setPrettyPrinting()
            .serializeNulls()
            .registerTypeAdapter(Date.class, typeAdapter)
            .create();
    msgConverter.setGson(gson);
    // Need for correct configuration of the swagger ui
    Jackson2ObjectMapperBuilder builder = Jackson2ObjectMapperBuilder.json();
    ObjectMapper mapper = builder.build().setDateFormat(typeAdapter.getDateFormat());
    converters.add(
        new MappingJackson2HttpMessageConverter(mapper) {
          @Override
          protected void writeInternal(Object t, HttpOutputMessage outputMessage)
              throws IOException, HttpMessageNotWritableException {
            super.writeInternal(t, outputMessage);
          }
        });
    converters.add(msgConverter);
  }

  @Override
  public void addInterceptors(InterceptorRegistry registry) {
    super.addInterceptors(registry);
    registry.addInterceptor(new TimerRequestInterceptor(timerService));
  }
}

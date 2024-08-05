package com.egalacoral.spark.timeform.api.multiplexer;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormAPI;
import com.egalacoral.spark.timeform.api.TimeFormService;
import com.egalacoral.spark.timeform.api.tools.Tools;
import java.lang.reflect.Proxy;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TimeFormAPIMultiplexer implements TimeFormAPI {

  private static final transient Logger LOGGER =
      LoggerFactory.getLogger(TimeFormAPIMultiplexer.class);

  private final TimeFormAPI firstApi;

  private final TimeFormAPI secondApi;

  public TimeFormAPIMultiplexer(TimeFormAPI firstApi, TimeFormAPI secondApi) {
    this.firstApi = firstApi;
    this.secondApi = secondApi;
  }

  @Override
  public TimeFormService login(String userName, String password) {
    TimeFormService service1 = firstApi.login(userName, password);
    TimeFormService service2 = secondApi.login(userName, password);

    return (TimeFormService)
        Proxy.newProxyInstance( //
            TimeFormAPIMultiplexer.class.getClassLoader(), //
            new Class[] {TimeFormService.class}, //
            (proxy, method, args) -> {
              Optional<Object> optionalCallback =
                  Tools.arrayToStream(args).filter(arg -> arg instanceof DataCallback).findFirst();
              if (optionalCallback.isPresent()) {
                DataCallback realCallback = (DataCallback) optionalCallback.get();
                List result = new ArrayList();
                LOGGER.info("Detected call to emulator");
                DataCallback<List> secondCallback =
                    new DataCallback<List>() {
                      @Override
                      public void onResponse(List data) {
                        LOGGER.debug("Second service returned {} rows", data.size());
                        result.addAll(data);
                        realCallback.onResponse(result);
                      }

                      @Override
                      public void onError(Exception e) {
                        realCallback.onError(e);
                      }
                    };

                DataCallback firstCallback =
                    new DataCallback() {
                      @Override
                      public void onResponse(Object data) {
                        if (data instanceof List) {
                          List list = (List) data;
                          LOGGER.debug("First service returned {} rows", list.size());
                          result.addAll(list);
                          try {
                            method.invoke(service2, replaceCallback(args, secondCallback));
                          } catch (Exception e) {
                            LOGGER.error("", e);
                            realCallback.onError(e);
                          }
                        } else {
                          realCallback.onResponse(data);
                        }
                      }

                      @Override
                      public void onError(Exception e) {
                        realCallback.onError(e);
                      }
                    };

                try {
                  method.invoke(service1, replaceCallback(args, firstCallback));
                } catch (Exception e) {
                  realCallback.onError(e);
                }
                return null;
              } else {
                LOGGER.info("Detected simple call");
                method.invoke(service2, args);
                return method.invoke(service1, args);
              }
            });
  }

  private Object[] replaceCallback(Object[] params, DataCallback newCallback) {
    Object[] result = Arrays.copyOf(params, params.length);
    for (int i = 0; i < result.length; i++) {
      if (result[i] instanceof DataCallback) {
        result[i] = newCallback;
      }
    }
    return result;
  }
}

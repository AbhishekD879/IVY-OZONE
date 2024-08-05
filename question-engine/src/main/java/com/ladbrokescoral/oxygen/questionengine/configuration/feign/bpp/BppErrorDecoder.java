package com.ladbrokescoral.oxygen.questionengine.configuration.feign.bpp;

import com.ladbrokescoral.oxygen.questionengine.exception.InvalidBppTokenException;
import com.ladbrokescoral.oxygen.questionengine.exception.ThirdPartyException;
import feign.Response;
import feign.codec.ErrorDecoder;
import java.nio.charset.StandardCharsets;
import lombok.SneakyThrows;
import org.apache.commons.io.IOUtils;

public class BppErrorDecoder implements ErrorDecoder {

  @Override
  @SneakyThrows
  public Exception decode(String methodKey, Response response) {
    if (response.status() == 401) {
      throw new InvalidBppTokenException("Authentication failed. Invalid BPP token: " + 
          IOUtils.toString(response.body().asInputStream(), StandardCharsets.UTF_8));
    } else if (response.status() == 400 || response.status() == 404 || response.status() == 422) {
      throw new ThirdPartyException("BPP response error. Status code: " + response.status());
    }
    return new Default().decode(methodKey, response);
  }
}

package com.ladbrokescoral.oxygen.questionengine.crm;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.dto.crm.CoinRequest;
import com.ladbrokescoral.oxygen.questionengine.dto.crm.CoinResponse;
import com.ladbrokescoral.oxygen.questionengine.exception.CrmException;
import lombok.extern.slf4j.Slf4j;
import okhttp3.Interceptor;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;
import okio.Buffer;
import org.json.JSONObject;

import java.io.IOException;


@Slf4j
public class RetryInterceptor implements Interceptor {

    private int countOfRetry;
    ObjectMapper objectMapper = new ObjectMapper();

    private static final String RETRY_ERROR_CODE = "ER102";

    public RetryInterceptor(int countOfRetry) {
        this.countOfRetry = countOfRetry;
    }

    public Response intercept(Chain chain) throws IOException {
        Request request = chain.request();
        Request finalRequest = request;
        Try<Response> response = Try.of(() -> chain.proceed(finalRequest));
        for (int tryCount = 1; shouldRetry(response) && tryCount <= this.countOfRetry; tryCount++) {
            RequestBody requestBody = request.body();
            requestBody = processApplicationJsonRequestBody(requestBody, tryCount);
            Request.Builder requestBuilder = request.newBuilder();
            request = requestBuilder
                    .post(requestBody)
                    .build();
            Request finalRequest1 = request;
            response = Try.of(() -> chain.proceed(finalRequest1));
            log.info("Request to {} is not successful - {} attempt", request.url(), tryCount);
        }
        return response.orElseThrow(RuntimeException::new);
    }

    private boolean shouldRetry(Try<Response> response) throws IOException {
        if (response.hasError() || !response.getResponse().isSuccessful()) {
            return true;
        } else {
            String coinObject = response.getResponse().peekBody(Long.MAX_VALUE).string();
            CoinResponse coinResponse = objectMapper.readValue(coinObject, CoinResponse.class);
            log.info("RetryInterceptor coinResponse ::: {}", coinResponse);
            if (RETRY_ERROR_CODE.equalsIgnoreCase(coinResponse.getRewardErrorCode()))
                return true;
        }
        return false;
    }

    private RequestBody processApplicationJsonRequestBody(RequestBody requestBody, int tryCount) throws IOException {
        String customReq = bodyToString(requestBody);
        try {
            CoinRequest coinRequest = objectMapper.readValue(customReq, CoinRequest.class);
            log.info("processApplicationJsonRequestBody coinRequest ::: {}", coinRequest);
            JSONObject obj = new JSONObject(customReq);
            obj.put("requestReferenceId", coinRequest.getRequestReferenceId() + "_" + tryCount);
            return RequestBody.create(obj.toString(), requestBody.contentType());
        } catch (Exception e) {
            log.error("Error while processApplicationJsonRequestBody {}", e.getMessage());
            throw new CrmException(e.getMessage());
        }
    }

    private String bodyToString(final RequestBody request) throws IOException {
        try (Buffer buffer = new Buffer()) {
            final RequestBody copy = request;
            if (copy != null)
                copy.writeTo(buffer);
            else
                return "";
            return buffer.readUtf8();
        }
    }
}

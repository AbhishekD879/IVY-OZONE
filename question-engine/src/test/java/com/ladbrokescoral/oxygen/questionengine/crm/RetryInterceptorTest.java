package com.ladbrokescoral.oxygen.questionengine.crm;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.dto.crm.CoinRequest;
import com.ladbrokescoral.oxygen.questionengine.exception.CrmException;
import okhttp3.*;
import org.json.JSONObject;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.stream.Collectors;

import static io.restassured.http.ContentType.JSON;
import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

public class RetryInterceptorTest {
    @Mock
    private Interceptor.Chain mockChain;

    @Before
    public void setUp() {
        MockitoAnnotations.initMocks(this);
    }

    @Test
    public void testInterceptSuccessfulResponse() throws IOException {
        String coinObj = getResourceFileAsString("award.json").toString();
        Request request = new Request.Builder().url("https://example.com").build();
        Response successfulResponse =
                new Response.Builder()
                        .request(request)
                        .protocol(okhttp3.Protocol.HTTP_1_1)
                        .code(200)
                        .message("OK")
                        .body(ResponseBody.create(okhttp3.MediaType.parse("text/plain"), coinObj))
                        .build();
        when(mockChain.request()).thenReturn(request);
        when(mockChain.proceed(request)).thenReturn(successfulResponse);
        RetryInterceptor interceptor = new RetryInterceptor(1);
        Response response = interceptor.intercept(mockChain);
        assertEquals(successfulResponse, response);
    }

    @Test
    public void testInterceptNotSuccessful() throws IOException, NoSuchMethodException {
        String coinObj = getResourceFileAsString("award.json").toString();
        Request request = createRequest();
        Response successfulResponse =
                new Response.Builder()
                        .request(request)
                        .protocol(okhttp3.Protocol.HTTP_1_1)
                        .code(404)
                        .message("NOT Found")
                        .body(ResponseBody.create(okhttp3.MediaType.parse("text/plain"), coinObj))
                        .build();
        when(mockChain.request()).thenReturn(request);
        when(mockChain.proceed(any())).thenReturn(successfulResponse);
        RetryInterceptor interceptor = new RetryInterceptor(1);
        Response response = interceptor.intercept(mockChain);
        assertEquals(successfulResponse, response);
    }

    @Test
    public void testInterceptSucesResRetryErrorCode() throws IOException {
        String coinObj = getResourceFileAsString("awardRetryErro.json").toString();
        Request request = createRequest();
        Response successfulResponse =
                new Response.Builder()
                        .request(request)
                        .protocol(okhttp3.Protocol.HTTP_1_1)
                        .code(200)
                        .message("OK")
                        .body(ResponseBody.create(okhttp3.MediaType.parse("text/plain"), coinObj))
                        .build();
        when(mockChain.request()).thenReturn(request);
        when(mockChain.proceed(any())).thenReturn(successfulResponse);
        RetryInterceptor interceptor = new RetryInterceptor(1);
        Response response = interceptor.intercept(mockChain);
        assertEquals(successfulResponse, response);
    }

    @Test(expected = RuntimeException.class)
    public void testInterceptWithMaxRetriesReached() throws IOException {
        Request request = createRequest();
        when(mockChain.request()).thenReturn(request);
        when(mockChain.proceed(any())).thenThrow(new IOException("Connection error"));
        RetryInterceptor interceptor = new RetryInterceptor(2);
        interceptor.intercept(mockChain);
    }

    @Test(expected = CrmException.class)
    public void testInterceptWithException() throws IOException {
        Request request = new Request.Builder().url("https://example.com").build();
        when(mockChain.request()).thenReturn(request);
        when(mockChain.proceed(any())).thenThrow(new IOException("Connection error"));
        RetryInterceptor interceptor = new RetryInterceptor(2);
        interceptor.intercept(mockChain);
    }

    protected String getResourceFileAsString(String resourceFileName) {
        InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));
        return reader.lines().collect(Collectors.joining("\n"));
    }

    Request createRequest() {
        String coinRequest = getResourceFileAsString("coinrequest.json").toString();
        MediaType JSON
                = MediaType.parse("application/json; charset=utf-8");
        RequestBody body = RequestBody.create(JSON, coinRequest.toString());
        Request request = new Request.Builder()
                .url("https://example.com")
                .post(body)
                .build();
        return request;
    }

}

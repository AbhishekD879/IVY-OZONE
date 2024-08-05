package com.ladbrokescoral.oxygen.questionengine.configuration;


import com.ladbrokescoral.oxygen.questionengine.crm.CrmService;
import com.ladbrokescoral.oxygen.questionengine.crm.CrmServiceImpl;
import lombok.extern.slf4j.Slf4j;
import okhttp3.OkHttpClient;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.IOException;
import java.security.KeyManagementException;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.UnrecoverableKeyException;
import java.security.cert.CertificateException;

@Slf4j(topic = "CRMOkHttp")
@Configuration
@ConditionalOnProperty(
        prefix = "crm",
        value = "enabled",
        havingValue = "true",
        matchIfMissing = false)
public class CrmConfiguration {

    private static final int MAX_IDLE_CONNECTIONS = 1;
    private static final int KEEP_ALIVE_DURATION = 60;
    private static final String PROXY_HOST = null;
    private static final String PROXY_PORT = null;

    @Bean
    @Qualifier("crmHttpClient")
    public OkHttpClient crmHttpClient(
            @Value("${crm.timeout.read:2}") int readTimeout,
            @Value("${crm.timeout.connect:2}") int connectTimeout,
            @Value("${crm.logging.level:BASIC}") String cmsLoggingLevel,
            OkHttpClientCreator okHttpClientCreator,
            @Value("${crm.count.retry:3}") int countOfRetry)
            throws KeyManagementException, NoSuchAlgorithmException, UnrecoverableKeyException, KeyStoreException, CertificateException, IOException {
        return okHttpClientCreator.createOkHttpClient(
                connectTimeout,
                readTimeout,
                MAX_IDLE_CONNECTIONS,
                KEEP_ALIVE_DURATION,
                log::info,
                cmsLoggingLevel,
                countOfRetry,
                PROXY_HOST,
                PROXY_PORT);
    }

}

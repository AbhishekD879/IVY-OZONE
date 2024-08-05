package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.ladbrokescoral.oxygen.questionengine.crm.RetryInterceptor;
import lombok.extern.slf4j.Slf4j;
import okhttp3.ConnectionPool;
import okhttp3.OkHttpClient;
import okhttp3.OkHttpClient.Builder;
import okhttp3.logging.HttpLoggingInterceptor;
import org.apache.commons.io.FilenameUtils;
import org.apache.http.ssl.SSLContextBuilder;
import org.apache.logging.log4j.util.Strings;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.util.ResourceUtils;

import javax.net.ssl.*;
import java.io.*;
import java.net.InetSocketAddress;
import java.net.Proxy;
import java.net.Proxy.Type;
import java.net.URL;
import java.security.*;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.concurrent.TimeUnit;

@Component
@Slf4j
public class OkHttpClientCreator {

    @Value("${crm.api.ssl.key-store-location}")
    private String keyStoreLocation;

    @Value("${crm.api.ssl.key-store-password}")
    private String keyStorePassword;

    @Value("${crm.api.ssl.trust-store-location}")
    private String trustStoreLocation;

    @Value("${crm.api.ssl.trust-store-password}")
    private String trustStorePassword;

    @Value("${spring.profiles.active}")
    private String envProfile;

    public OkHttpClient createOkHttpClient(
            long connectionTimeout,
            long readTimeout,
            int maxIdleConnections,
            long keepAliveDuration,
            HttpLoggingInterceptor.Logger logger,
            String loggingLevel,
            int countOfRetry,
            String proxyHost,
            String proxyPort)
            throws NoSuchAlgorithmException, KeyManagementException, KeyStoreException, UnrecoverableKeyException, CertificateException, IOException {
        HttpLoggingInterceptor interceptor = new HttpLoggingInterceptor(logger);
        interceptor.setLevel(HttpLoggingInterceptor.Level.valueOf(loggingLevel));
        log.warn("**** Allow untrusted SSL connection ****");
        final TrustManager[] listOfTrustManagers = new TrustManager[]{new BlindTrustManager()};
        log.info("OkHttpClientCreator keyStoreLocation {} ", keyStoreLocation);
        log.info("OkHttpClientCreator trustStoreLocation {} ", trustStoreLocation);
        SSLContext sslContext = SSLContext.getInstance("TLSv1.2");
        KeyStore keyStore = readKeyStore(keyStoreLocation);
        KeyManagerFactory keyManagerFactory = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        keyManagerFactory.init(keyStore, keyStorePassword.toCharArray());
        KeyStore trustStore = readKeyStore(trustStoreLocation);
        TrustManagerFactory trustManagerFactory = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        trustManagerFactory.init(trustStore);
        Builder clientBuilder = null;
        if (!envProfile.equalsIgnoreCase("STG0")) {
            //Allowing trust store certs in beta/prod env
            sslContext.init(keyManagerFactory.getKeyManagers(), trustManagerFactory.getTrustManagers(), new java.security.SecureRandom());
            clientBuilder =
                    new Builder()
                            .addInterceptor(new RetryInterceptor(countOfRetry))
                            .connectionPool(
                                    new ConnectionPool(maxIdleConnections, keepAliveDuration, TimeUnit.SECONDS))
                            .retryOnConnectionFailure(false)
                            .readTimeout(readTimeout, TimeUnit.SECONDS)
                            .connectTimeout(connectionTimeout, TimeUnit.SECONDS)
                            .proxy(Proxy.NO_PROXY)
                            .sslSocketFactory(
                                    sslContext.getSocketFactory(), (X509TrustManager) trustManagerFactory.getTrustManagers()[0])
                            .hostnameVerifier(OkHttpClientCreator::hostNameSessionVerifier);

        } else {
            //Ignoring trust store certs in stg env
            sslContext.init(keyManagerFactory.getKeyManagers(), listOfTrustManagers, new java.security.SecureRandom());
            clientBuilder =
                    new Builder()
                            .addInterceptor(new RetryInterceptor(countOfRetry))
                            .connectionPool(
                                    new ConnectionPool(maxIdleConnections, keepAliveDuration, TimeUnit.SECONDS))
                            .retryOnConnectionFailure(false)
                            .readTimeout(readTimeout, TimeUnit.SECONDS)
                            .connectTimeout(connectionTimeout, TimeUnit.SECONDS)
                            .proxy(Proxy.NO_PROXY)
                            .sslSocketFactory(
                                    sslContext.getSocketFactory(), (X509TrustManager) listOfTrustManagers[0])
                            .hostnameVerifier(OkHttpClientCreator::hostNameSessionVerifier);
        }
        if (Strings.isNotBlank(proxyHost) && Strings.isNotBlank(proxyPort)) {
            return clientBuilder
                    .proxy(
                            new Proxy(Type.HTTP, new InetSocketAddress(proxyHost, Integer.parseInt(proxyPort))))
                    .build();
        }
        return clientBuilder.build();
    }

    KeyStore readKeyStore(String keyStorePath) throws IOException, KeyStoreException, CertificateException, NoSuchAlgorithmException {
        File file = ResourceUtils.getFile(keyStorePath);
        try (InputStream keyStoreStream = new FileInputStream(file)) {
            KeyStore keyStore = KeyStore.getInstance("JKS");
            keyStore.load(keyStoreStream, keyStorePassword.toCharArray());
            return keyStore;
        }
    }

    public static boolean hostNameSessionVerifier(String hostname, SSLSession sslSession) {
        return (hostname != null && sslSession != null);
    }

    static class BlindTrustManager implements X509TrustManager {
        @Override
        public X509Certificate[] getAcceptedIssuers() {
            return new X509Certificate[0];
        }

        @Override
        public void checkServerTrusted(final X509Certificate[] chain, final String authType) throws CertificateException {
            if (chain == null || chain.length == 0)
                throw new CertificateException("No X509TrustManager implementation available");
        }

        @Override
        public void checkClientTrusted(final X509Certificate[] chain, final String authType) throws CertificateException {
            if (chain == null || chain.length == 0)
                throw new CertificateException("No X509TrustManager implementation available");
        }
    }
}

package com.coral.oxygen.middleware.common.configuration.cfcache;

public interface DeliveryNetworkService {

  <T> void upload(String brand, String path, String fileName, T object);
}

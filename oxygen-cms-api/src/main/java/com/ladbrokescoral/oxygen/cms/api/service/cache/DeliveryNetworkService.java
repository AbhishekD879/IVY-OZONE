package com.ladbrokescoral.oxygen.cms.api.service.cache;

public interface DeliveryNetworkService {

  <T> void upload(String brand, String path, String fileName, T object);

  void delete(String brand, String path, String fileName);

  <T> void uploadCFContent(String brand, String path, String fileName, T object);
}

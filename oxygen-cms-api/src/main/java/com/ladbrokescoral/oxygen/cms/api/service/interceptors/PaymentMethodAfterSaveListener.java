package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.PaymentMethodDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PaymentMethod;
import com.ladbrokescoral.oxygen.cms.api.service.PaymentMethodService;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;
import org.springframework.stereotype.Component;

@Component
public class PaymentMethodAfterSaveListener extends BasicMongoEventListener<PaymentMethod> {

  private final PaymentMethodService service;
  private static final String PATH_TEMPLATE = "api/{0}/";
  private static final String FILE_NAME = "payment-methods";

  public PaymentMethodAfterSaveListener(
      final PaymentMethodService service, final DeliveryNetworkService context) {
    super(context);
    this.service = service;
  }

  @Override
  public void onAfterSave(AfterSaveEvent<PaymentMethod> event) {
    String brand = event.getSource().getBrand();
    List<PaymentMethod> content = (List<PaymentMethod>) service.findByBrand(brand);
    uploadCollection(
        brand,
        PATH_TEMPLATE,
        FILE_NAME,
        content.stream()
            .map(
                s ->
                    new PaymentMethodDto(
                        s.isActive(), s.getName(), s.getIdentifier(), s.getSortOrder()))
            .collect(Collectors.toList()));
  }
}

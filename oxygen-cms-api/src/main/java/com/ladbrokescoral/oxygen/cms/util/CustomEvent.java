package com.ladbrokescoral.oxygen.cms.util;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import lombok.Getter;
import lombok.Setter;
import org.springframework.context.ApplicationEvent;
import org.springframework.core.ResolvableType;
import org.springframework.core.ResolvableTypeProvider;

@Setter
@Getter
public class CustomEvent<T extends HasBrand> extends ApplicationEvent
    implements ResolvableTypeProvider {
  private String collectionName;

  private String brand;
  /**
   * Create a new {@code ApplicationEvent}.
   *
   * @param source the object on which the event initially occurred or with which the event is
   *     associated (never {@code null})
   */
  public CustomEvent(T source, String collectionName, String brand) {
    super(source);
    this.collectionName = collectionName;
    this.brand = brand;
  }

  @Override
  public ResolvableType getResolvableType() {
    return ResolvableType.forClassWithGenerics(getClass(), ResolvableType.forInstance(getSource()));
  }
}

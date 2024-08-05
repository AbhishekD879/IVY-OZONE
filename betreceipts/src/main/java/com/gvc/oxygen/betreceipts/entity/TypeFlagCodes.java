package com.gvc.oxygen.betreceipts.entity;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.springframework.util.ObjectUtils;

public class TypeFlagCodes {

  private static final String DELIMITER = ",";

  private List<String> codes = new ArrayList<>();

  private TypeFlagCodes(List<String> codes) {
    this.codes = codes;
  }

  private TypeFlagCodes() {
    super();
  }

  public static TypeFlagCodes of(String typeFlagCodes) {
    TypeFlagCodes codes;
    if (!ObjectUtils.isEmpty(typeFlagCodes)) {
      String[] array = typeFlagCodes.split(DELIMITER);
      codes = of(array);
    } else {
      codes = new TypeFlagCodes();
    }
    return codes;
  }

  public static TypeFlagCodes of(String... array) {
    List<String> codes = Arrays.asList(array);
    return new TypeFlagCodes(codes);
  }

  public String toString() {
    return codes.stream().collect(Collectors.joining(DELIMITER));
  }

  public boolean contains(TypeFlagCodes of) {
    return codes.stream().filter(of.codes::contains).count() > 0;
  }

  public List<String> getCodes() {
    return Collections.unmodifiableList(codes);
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }
    TypeFlagCodes codes1 = (TypeFlagCodes) o;
    return codes.equals(codes1.codes);
  }

  @Override
  public int hashCode() {
    return Objects.hash(codes);
  }
}

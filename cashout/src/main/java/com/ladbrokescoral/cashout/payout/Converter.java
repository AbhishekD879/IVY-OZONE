package com.ladbrokescoral.cashout.payout;

public interface Converter<S, T> {
  T convert(S source);
}

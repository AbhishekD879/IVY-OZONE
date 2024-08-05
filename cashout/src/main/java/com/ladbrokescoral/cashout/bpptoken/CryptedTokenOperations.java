package com.ladbrokescoral.cashout.bpptoken;

public class CryptedTokenOperations implements BppTokenOperations {
  private final BppTokenOperations tokenOperations;
  private final CryptOperations cryptOperations;

  public CryptedTokenOperations(
      BppTokenOperations tokenOperations, CryptOperations cryptOperations) {
    this.tokenOperations = tokenOperations;
    this.cryptOperations = cryptOperations;
  }

  @Override
  public BppToken parseToken(String token) {
    BppToken bppToken = tokenOperations.parseToken(cryptOperations.decrypt(token));
    return bppToken.toBuilder().token(token).build();
  }
}

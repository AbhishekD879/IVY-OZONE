package com.ladbrokescoral.oxygen.questionengine.service;

import java.util.List;

public abstract class AbstractDataSource<T> {

    private static final Integer ZERO = 0;
    public abstract void addAll(List<T> t);
    public void delete(T t){}
    public void clear(){}
    public T getPeek(){ return null;}
    public T getPoll(){ return null; }
    public abstract Boolean isEmpty();
    public int size(){ return ZERO; }

}

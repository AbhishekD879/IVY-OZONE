//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for complexLeg complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="complexLeg">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="outcomeCombiRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded"/>
 *         &lt;element name="outcomeRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded"/>
 *         &lt;element name="price" type="{http://schema.products.sportsbook.openbet.com/betcommon}price"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "complexLeg", propOrder = {
    "outcomeCombiRef",
    "outcomeRef",
    "price"
})
public class ComplexLeg
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    @XmlElement(required = true)
    protected List<EntityRef> outcomeCombiRef;
    @XmlElement(required = true)
    protected List<EntityRef> outcomeRef;
    @XmlElement(required = true)
    protected Price price;

    /**
     * Gets the value of the outcomeCombiRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the outcomeCombiRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOutcomeCombiRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getOutcomeCombiRef() {
        if (outcomeCombiRef == null) {
            outcomeCombiRef = new ArrayList<EntityRef>();
        }
        return this.outcomeCombiRef;
    }

    public boolean isSetOutcomeCombiRef() {
        return ((this.outcomeCombiRef!= null)&&(!this.outcomeCombiRef.isEmpty()));
    }

    public void unsetOutcomeCombiRef() {
        this.outcomeCombiRef = null;
    }

    /**
     * Gets the value of the outcomeRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the outcomeRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOutcomeRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getOutcomeRef() {
        if (outcomeRef == null) {
            outcomeRef = new ArrayList<EntityRef>();
        }
        return this.outcomeRef;
    }

    public boolean isSetOutcomeRef() {
        return ((this.outcomeRef!= null)&&(!this.outcomeRef.isEmpty()));
    }

    public void unsetOutcomeRef() {
        this.outcomeRef = null;
    }

    /**
     * Gets the value of the price property.
     * 
     * @return
     *     possible object is
     *     {@link Price }
     *     
     */
    public Price getPrice() {
        return price;
    }

    /**
     * Sets the value of the price property.
     * 
     * @param value
     *     allowed object is
     *     {@link Price }
     *     
     */
    public void setPrice(Price value) {
        this.price = value;
    }

    public boolean isSetPrice() {
        return (this.price!= null);
    }

}
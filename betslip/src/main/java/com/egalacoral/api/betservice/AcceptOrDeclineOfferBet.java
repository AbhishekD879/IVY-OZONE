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
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlType;


/**
 * <p>Java class for anonymous complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType>
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="customerRef" type="{http://schema.openbet.com/core}entityRef"/>
 *         &lt;element name="offerBetAction" type="{http://schema.products.sportsbook.openbet.com/bet}offerBetAction" maxOccurs="unbounded"/>
 *       &lt;/sequence>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
    "customerRef",
    "offerBetAction"
})
@XmlRootElement(name = "acceptOrDeclineOfferBet")
public class AcceptOrDeclineOfferBet
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    @XmlElement(required = true)
    protected EntityRef customerRef;
    @XmlElement(required = true)
    protected List<OfferBetAction> offerBetAction;

    /**
     * Gets the value of the customerRef property.
     * 
     * @return
     *     possible object is
     *     {@link EntityRef }
     *     
     */
    public EntityRef getCustomerRef() {
        return customerRef;
    }

    /**
     * Sets the value of the customerRef property.
     * 
     * @param value
     *     allowed object is
     *     {@link EntityRef }
     *     
     */
    public void setCustomerRef(EntityRef value) {
        this.customerRef = value;
    }

    public boolean isSetCustomerRef() {
        return (this.customerRef!= null);
    }

    /**
     * Gets the value of the offerBetAction property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the offerBetAction property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getOfferBetAction().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link OfferBetAction }
     * 
     * 
     */
    public List<OfferBetAction> getOfferBetAction() {
        if (offerBetAction == null) {
            offerBetAction = new ArrayList<OfferBetAction>();
        }
        return this.offerBetAction;
    }

    public boolean isSetOfferBetAction() {
        return ((this.offerBetAction!= null)&&(!this.offerBetAction.isEmpty()));
    }

    public void unsetOfferBetAction() {
        this.offerBetAction = null;
    }

}
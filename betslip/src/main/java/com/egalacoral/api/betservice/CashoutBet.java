//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAttribute;
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
 *         &lt;element name="customerRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *         &lt;element name="betRef" type="{http://schema.openbet.com/core}entityRef"/>
 *         &lt;element name="channelRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *         &lt;element name="cashoutValue" type="{http://schema.products.sportsbook.openbet.com/bet}cashoutValue"/>
 *         &lt;element name="betInfo" type="{http://schema.products.sportsbook.openbet.com/bet}slipPlacementInfo" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attribute name="adminMode" type="{http://schema.openbet.com/core}yesNo" />
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
    "betRef",
    "channelRef",
    "cashoutValue",
    "betInfo"
})
@XmlRootElement(name = "cashoutBet")
public class CashoutBet
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    protected EntityRef customerRef;
    @XmlElement(required = true)
    protected EntityRef betRef;
    protected EntityRef channelRef;
    @XmlElement(required = true)
    protected CashoutValue cashoutValue;
    protected SlipPlacementInfo betInfo;
    @XmlAttribute
    protected YesNo adminMode;

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
     * Gets the value of the betRef property.
     * 
     * @return
     *     possible object is
     *     {@link EntityRef }
     *     
     */
    public EntityRef getBetRef() {
        return betRef;
    }

    /**
     * Sets the value of the betRef property.
     * 
     * @param value
     *     allowed object is
     *     {@link EntityRef }
     *     
     */
    public void setBetRef(EntityRef value) {
        this.betRef = value;
    }

    public boolean isSetBetRef() {
        return (this.betRef!= null);
    }

    /**
     * Gets the value of the channelRef property.
     * 
     * @return
     *     possible object is
     *     {@link EntityRef }
     *     
     */
    public EntityRef getChannelRef() {
        return channelRef;
    }

    /**
     * Sets the value of the channelRef property.
     * 
     * @param value
     *     allowed object is
     *     {@link EntityRef }
     *     
     */
    public void setChannelRef(EntityRef value) {
        this.channelRef = value;
    }

    public boolean isSetChannelRef() {
        return (this.channelRef!= null);
    }

    /**
     * Gets the value of the cashoutValue property.
     * 
     * @return
     *     possible object is
     *     {@link CashoutValue }
     *     
     */
    public CashoutValue getCashoutValue() {
        return cashoutValue;
    }

    /**
     * Sets the value of the cashoutValue property.
     * 
     * @param value
     *     allowed object is
     *     {@link CashoutValue }
     *     
     */
    public void setCashoutValue(CashoutValue value) {
        this.cashoutValue = value;
    }

    public boolean isSetCashoutValue() {
        return (this.cashoutValue!= null);
    }

    /**
     * Gets the value of the betInfo property.
     * 
     * @return
     *     possible object is
     *     {@link SlipPlacementInfo }
     *     
     */
    public SlipPlacementInfo getBetInfo() {
        return betInfo;
    }

    /**
     * Sets the value of the betInfo property.
     * 
     * @param value
     *     allowed object is
     *     {@link SlipPlacementInfo }
     *     
     */
    public void setBetInfo(SlipPlacementInfo value) {
        this.betInfo = value;
    }

    public boolean isSetBetInfo() {
        return (this.betInfo!= null);
    }

    /**
     * Gets the value of the adminMode property.
     * 
     * @return
     *     possible object is
     *     {@link YesNo }
     *     
     */
    public YesNo getAdminMode() {
        return adminMode;
    }

    /**
     * Sets the value of the adminMode property.
     * 
     * @param value
     *     allowed object is
     *     {@link YesNo }
     *     
     */
    public void setAdminMode(YesNo value) {
        this.adminMode = value;
    }

    public boolean isSetAdminMode() {
        return (this.adminMode!= null);
    }

}

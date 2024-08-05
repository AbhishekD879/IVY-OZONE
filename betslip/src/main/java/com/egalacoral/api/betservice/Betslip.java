//
// This file was generated by the JavaTM Architecture for XML Binding(JAXB) Reference Implementation, vhudson-jaxb-ri-2.1-558 
// See <a href="http://java.sun.com/xml/jaxb">http://java.sun.com/xml/jaxb</a> 
// Any modifications to this file will be lost upon recompilation of the source schema. 
// Generated on: 2016.04.20 at 09:40:42 PM EEST 
//


package com.egalacoral.api.betservice;

import java.io.Serializable;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlAnyAttribute;
import javax.xml.bind.annotation.XmlAttribute;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlSchemaType;
import javax.xml.bind.annotation.XmlType;
import javax.xml.datatype.XMLGregorianCalendar;
import javax.xml.namespace.QName;


/**
 * 
 * 				Each bet will be associated with a slip. This would
 * 				normally be a grouping of bets placed at the same time but each bet
 * 				could be stored against its own slip. The funding of the bets is done
 * 				at the slip level.
 * 			
 * 
 * <p>Java class for betslip complex type.
 * 
 * <p>The following schema fragment specifies the expected content contained within this class.
 * 
 * <pre>
 * &lt;complexType name="betslip">
 *   &lt;complexContent>
 *     &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *       &lt;sequence>
 *         &lt;element name="externalRef" type="{http://schema.products.sportsbook.openbet.com/bet}externalRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="errorRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *         &lt;element name="stake" type="{http://schema.products.sportsbook.openbet.com/bet}betStake"/>
 *         &lt;element name="customerRef" type="{http://schema.openbet.com/core}entityRef"/>
 *         &lt;element name="anonTagRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *         &lt;element name="affiliateRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *         &lt;element name="slipPlacement" type="{http://schema.products.sportsbook.openbet.com/bet}slipPlacementInfo"/>
 *         &lt;element name="slipCapture" minOccurs="0">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element name="operatorRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *                 &lt;/sequence>
 *                 &lt;attribute name="timeStamp" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *         &lt;element name="slipCollection" minOccurs="0">
 *           &lt;complexType>
 *             &lt;complexContent>
 *               &lt;restriction base="{http://www.w3.org/2001/XMLSchema}anyType">
 *                 &lt;sequence>
 *                   &lt;element name="shopRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *                   &lt;element name="operatorRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
 *                 &lt;/sequence>
 *                 &lt;attribute name="timeStamp" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
 *                 &lt;attribute name="amount" type="{http://www.w3.org/2001/XMLSchema}decimal" />
 *               &lt;/restriction>
 *             &lt;/complexContent>
 *           &lt;/complexType>
 *         &lt;/element>
 *         &lt;element name="betRef" type="{http://schema.openbet.com/core}entityRef" maxOccurs="unbounded" minOccurs="0"/>
 *       &lt;/sequence>
 *       &lt;attGroup ref="{http://schema.openbet.com/core}entityAttrGroup"/>
 *       &lt;attribute name="barcode" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="loyaltyCard" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="receipt" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="isAccountBet" type="{http://schema.openbet.com/core}yesNo" default="Y" />
 *       &lt;attribute name="isHedgedBet" type="{http://schema.openbet.com/core}yesNo" default="N" />
 *       &lt;attribute name="betGroupType" type="{http://www.w3.org/2001/XMLSchema}string" />
 *       &lt;attribute name="clientUserAgent">
 *         &lt;simpleType>
 *           &lt;restriction base="{http://www.w3.org/2001/XMLSchema}string">
 *             &lt;maxLength value="12"/>
 *           &lt;/restriction>
 *         &lt;/simpleType>
 *       &lt;/attribute>
 *     &lt;/restriction>
 *   &lt;/complexContent>
 * &lt;/complexType>
 * </pre>
 * 
 * 
 */
@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "betslip", propOrder = {
    "externalRef",
    "errorRef",
    "stake",
    "customerRef",
    "anonTagRef",
    "affiliateRef",
    "slipPlacement",
    "slipCapture",
    "slipCollection",
    "betRef"
})
public class Betslip
    implements Serializable
{

    private final static long serialVersionUID = 1L;
    protected List<ExternalRef> externalRef;
    protected List<EntityRef> errorRef;
    @XmlElement(required = true)
    protected BetStake stake;
    @XmlElement(required = true)
    protected EntityRef customerRef;
    protected EntityRef anonTagRef;
    protected EntityRef affiliateRef;
    @XmlElement(required = true)
    protected SlipPlacementInfo slipPlacement;
    protected SlipCapture slipCapture;
    protected SlipCollection slipCollection;
    protected List<EntityRef> betRef;
    @XmlAttribute
    protected String barcode;
    @XmlAttribute
    protected String loyaltyCard;
    @XmlAttribute
    protected String receipt;
    @XmlAttribute
    protected YesNo isAccountBet;
    @XmlAttribute
    protected YesNo isHedgedBet;
    @XmlAttribute
    protected String betGroupType;
    @XmlAttribute
    protected String clientUserAgent;
    @XmlAttribute
    protected String id;
    @XmlAttribute
    protected String documentId;
    @XmlAttribute
    protected String provider;
    @XmlAttribute
    protected String addr;
    @XmlAttribute
    protected String version;
    @XmlAttribute
    @XmlSchemaType(name = "positiveInteger")
    protected BigInteger ordering;
    @XmlAnyAttribute
    private Map<QName, String> otherAttributes = new HashMap<QName, String>();

    /**
     * Gets the value of the externalRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the externalRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getExternalRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link ExternalRef }
     * 
     * 
     */
    public List<ExternalRef> getExternalRef() {
        if (externalRef == null) {
            externalRef = new ArrayList<ExternalRef>();
        }
        return this.externalRef;
    }

    public boolean isSetExternalRef() {
        return ((this.externalRef!= null)&&(!this.externalRef.isEmpty()));
    }

    public void unsetExternalRef() {
        this.externalRef = null;
    }

    /**
     * Gets the value of the errorRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the errorRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getErrorRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getErrorRef() {
        if (errorRef == null) {
            errorRef = new ArrayList<EntityRef>();
        }
        return this.errorRef;
    }

    public boolean isSetErrorRef() {
        return ((this.errorRef!= null)&&(!this.errorRef.isEmpty()));
    }

    public void unsetErrorRef() {
        this.errorRef = null;
    }

    /**
     * Gets the value of the stake property.
     * 
     * @return
     *     possible object is
     *     {@link BetStake }
     *     
     */
    public BetStake getStake() {
        return stake;
    }

    /**
     * Sets the value of the stake property.
     * 
     * @param value
     *     allowed object is
     *     {@link BetStake }
     *     
     */
    public void setStake(BetStake value) {
        this.stake = value;
    }

    public boolean isSetStake() {
        return (this.stake!= null);
    }

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
     * Gets the value of the anonTagRef property.
     * 
     * @return
     *     possible object is
     *     {@link EntityRef }
     *     
     */
    public EntityRef getAnonTagRef() {
        return anonTagRef;
    }

    /**
     * Sets the value of the anonTagRef property.
     * 
     * @param value
     *     allowed object is
     *     {@link EntityRef }
     *     
     */
    public void setAnonTagRef(EntityRef value) {
        this.anonTagRef = value;
    }

    public boolean isSetAnonTagRef() {
        return (this.anonTagRef!= null);
    }

    /**
     * Gets the value of the affiliateRef property.
     * 
     * @return
     *     possible object is
     *     {@link EntityRef }
     *     
     */
    public EntityRef getAffiliateRef() {
        return affiliateRef;
    }

    /**
     * Sets the value of the affiliateRef property.
     * 
     * @param value
     *     allowed object is
     *     {@link EntityRef }
     *     
     */
    public void setAffiliateRef(EntityRef value) {
        this.affiliateRef = value;
    }

    public boolean isSetAffiliateRef() {
        return (this.affiliateRef!= null);
    }

    /**
     * Gets the value of the slipPlacement property.
     * 
     * @return
     *     possible object is
     *     {@link SlipPlacementInfo }
     *     
     */
    public SlipPlacementInfo getSlipPlacement() {
        return slipPlacement;
    }

    /**
     * Sets the value of the slipPlacement property.
     * 
     * @param value
     *     allowed object is
     *     {@link SlipPlacementInfo }
     *     
     */
    public void setSlipPlacement(SlipPlacementInfo value) {
        this.slipPlacement = value;
    }

    public boolean isSetSlipPlacement() {
        return (this.slipPlacement!= null);
    }

    /**
     * Gets the value of the slipCapture property.
     * 
     * @return
     *     possible object is
     *     {@link SlipCapture }
     *     
     */
    public SlipCapture getSlipCapture() {
        return slipCapture;
    }

    /**
     * Sets the value of the slipCapture property.
     * 
     * @param value
     *     allowed object is
     *     {@link SlipCapture }
     *     
     */
    public void setSlipCapture(SlipCapture value) {
        this.slipCapture = value;
    }

    public boolean isSetSlipCapture() {
        return (this.slipCapture!= null);
    }

    /**
     * Gets the value of the slipCollection property.
     * 
     * @return
     *     possible object is
     *     {@link SlipCollection }
     *     
     */
    public SlipCollection getSlipCollection() {
        return slipCollection;
    }

    /**
     * Sets the value of the slipCollection property.
     * 
     * @param value
     *     allowed object is
     *     {@link SlipCollection }
     *     
     */
    public void setSlipCollection(SlipCollection value) {
        this.slipCollection = value;
    }

    public boolean isSetSlipCollection() {
        return (this.slipCollection!= null);
    }

    /**
     * Gets the value of the betRef property.
     * 
     * <p>
     * This accessor method returns a reference to the live list,
     * not a snapshot. Therefore any modification you make to the
     * returned list will be present inside the JAXB object.
     * This is why there is not a <CODE>set</CODE> method for the betRef property.
     * 
     * <p>
     * For example, to add a new item, do as follows:
     * <pre>
     *    getBetRef().add(newItem);
     * </pre>
     * 
     * 
     * <p>
     * Objects of the following type(s) are allowed in the list
     * {@link EntityRef }
     * 
     * 
     */
    public List<EntityRef> getBetRef() {
        if (betRef == null) {
            betRef = new ArrayList<EntityRef>();
        }
        return this.betRef;
    }

    public boolean isSetBetRef() {
        return ((this.betRef!= null)&&(!this.betRef.isEmpty()));
    }

    public void unsetBetRef() {
        this.betRef = null;
    }

    /**
     * Gets the value of the barcode property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getBarcode() {
        return barcode;
    }

    /**
     * Sets the value of the barcode property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setBarcode(String value) {
        this.barcode = value;
    }

    public boolean isSetBarcode() {
        return (this.barcode!= null);
    }

    /**
     * Gets the value of the loyaltyCard property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getLoyaltyCard() {
        return loyaltyCard;
    }

    /**
     * Sets the value of the loyaltyCard property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setLoyaltyCard(String value) {
        this.loyaltyCard = value;
    }

    public boolean isSetLoyaltyCard() {
        return (this.loyaltyCard!= null);
    }

    /**
     * Gets the value of the receipt property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getReceipt() {
        return receipt;
    }

    /**
     * Sets the value of the receipt property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setReceipt(String value) {
        this.receipt = value;
    }

    public boolean isSetReceipt() {
        return (this.receipt!= null);
    }

    /**
     * Gets the value of the isAccountBet property.
     * 
     * @return
     *     possible object is
     *     {@link YesNo }
     *     
     */
    public YesNo getIsAccountBet() {
        if (isAccountBet == null) {
            return YesNo.Y;
        } else {
            return isAccountBet;
        }
    }

    /**
     * Sets the value of the isAccountBet property.
     * 
     * @param value
     *     allowed object is
     *     {@link YesNo }
     *     
     */
    public void setIsAccountBet(YesNo value) {
        this.isAccountBet = value;
    }

    public boolean isSetIsAccountBet() {
        return (this.isAccountBet!= null);
    }

    /**
     * Gets the value of the isHedgedBet property.
     * 
     * @return
     *     possible object is
     *     {@link YesNo }
     *     
     */
    public YesNo getIsHedgedBet() {
        if (isHedgedBet == null) {
            return YesNo.N;
        } else {
            return isHedgedBet;
        }
    }

    /**
     * Sets the value of the isHedgedBet property.
     * 
     * @param value
     *     allowed object is
     *     {@link YesNo }
     *     
     */
    public void setIsHedgedBet(YesNo value) {
        this.isHedgedBet = value;
    }

    public boolean isSetIsHedgedBet() {
        return (this.isHedgedBet!= null);
    }

    /**
     * Gets the value of the betGroupType property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getBetGroupType() {
        return betGroupType;
    }

    /**
     * Sets the value of the betGroupType property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setBetGroupType(String value) {
        this.betGroupType = value;
    }

    public boolean isSetBetGroupType() {
        return (this.betGroupType!= null);
    }

    /**
     * Gets the value of the clientUserAgent property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getClientUserAgent() {
        return clientUserAgent;
    }

    /**
     * Sets the value of the clientUserAgent property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setClientUserAgent(String value) {
        this.clientUserAgent = value;
    }

    public boolean isSetClientUserAgent() {
        return (this.clientUserAgent!= null);
    }

    /**
     * Gets the value of the id property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getId() {
        return id;
    }

    /**
     * Sets the value of the id property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setId(String value) {
        this.id = value;
    }

    public boolean isSetId() {
        return (this.id!= null);
    }

    /**
     * Gets the value of the documentId property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getDocumentId() {
        return documentId;
    }

    /**
     * Sets the value of the documentId property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setDocumentId(String value) {
        this.documentId = value;
    }

    public boolean isSetDocumentId() {
        return (this.documentId!= null);
    }

    /**
     * Gets the value of the provider property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getProvider() {
        if (provider == null) {
            return "OpenBet";
        } else {
            return provider;
        }
    }

    /**
     * Sets the value of the provider property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setProvider(String value) {
        this.provider = value;
    }

    public boolean isSetProvider() {
        return (this.provider!= null);
    }

    /**
     * Gets the value of the addr property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getAddr() {
        return addr;
    }

    /**
     * Sets the value of the addr property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setAddr(String value) {
        this.addr = value;
    }

    public boolean isSetAddr() {
        return (this.addr!= null);
    }

    /**
     * Gets the value of the version property.
     * 
     * @return
     *     possible object is
     *     {@link String }
     *     
     */
    public String getVersion() {
        return version;
    }

    /**
     * Sets the value of the version property.
     * 
     * @param value
     *     allowed object is
     *     {@link String }
     *     
     */
    public void setVersion(String value) {
        this.version = value;
    }

    public boolean isSetVersion() {
        return (this.version!= null);
    }

    /**
     * Gets the value of the ordering property.
     * 
     * @return
     *     possible object is
     *     {@link BigInteger }
     *     
     */
    public BigInteger getOrdering() {
        return ordering;
    }

    /**
     * Sets the value of the ordering property.
     * 
     * @param value
     *     allowed object is
     *     {@link BigInteger }
     *     
     */
    public void setOrdering(BigInteger value) {
        this.ordering = value;
    }

    public boolean isSetOrdering() {
        return (this.ordering!= null);
    }

    /**
     * Gets a map that contains attributes that aren't bound to any typed property on this class.
     * 
     * <p>
     * the map is keyed by the name of the attribute and 
     * the value is the string value of the attribute.
     * 
     * the map returned by this method is live, and you can add new attribute
     * by updating the map directly. Because of this design, there's no setter.
     * 
     * 
     * @return
     *     always non-null
     */
    public Map<QName, String> getOtherAttributes() {
        return otherAttributes;
    }


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
     *         &lt;element name="operatorRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
     *       &lt;/sequence>
     *       &lt;attribute name="timeStamp" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "operatorRef"
    })
    public static class SlipCapture
        implements Serializable
    {

        private final static long serialVersionUID = 1L;
        protected EntityRef operatorRef;
        @XmlAttribute
        @XmlSchemaType(name = "dateTime")
        protected XMLGregorianCalendar timeStamp;
        @XmlAnyAttribute
        private Map<QName, String> otherAttributes = new HashMap<QName, String>();

        /**
         * Gets the value of the operatorRef property.
         * 
         * @return
         *     possible object is
         *     {@link EntityRef }
         *     
         */
        public EntityRef getOperatorRef() {
            return operatorRef;
        }

        /**
         * Sets the value of the operatorRef property.
         * 
         * @param value
         *     allowed object is
         *     {@link EntityRef }
         *     
         */
        public void setOperatorRef(EntityRef value) {
            this.operatorRef = value;
        }

        public boolean isSetOperatorRef() {
            return (this.operatorRef!= null);
        }

        /**
         * Gets the value of the timeStamp property.
         * 
         * @return
         *     possible object is
         *     {@link XMLGregorianCalendar }
         *     
         */
        public XMLGregorianCalendar getTimeStamp() {
            return timeStamp;
        }

        /**
         * Sets the value of the timeStamp property.
         * 
         * @param value
         *     allowed object is
         *     {@link XMLGregorianCalendar }
         *     
         */
        public void setTimeStamp(XMLGregorianCalendar value) {
            this.timeStamp = value;
        }

        public boolean isSetTimeStamp() {
            return (this.timeStamp!= null);
        }

        /**
         * Gets a map that contains attributes that aren't bound to any typed property on this class.
         * 
         * <p>
         * the map is keyed by the name of the attribute and 
         * the value is the string value of the attribute.
         * 
         * the map returned by this method is live, and you can add new attribute
         * by updating the map directly. Because of this design, there's no setter.
         * 
         * 
         * @return
         *     always non-null
         */
        public Map<QName, String> getOtherAttributes() {
            return otherAttributes;
        }

    }


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
     *         &lt;element name="shopRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
     *         &lt;element name="operatorRef" type="{http://schema.openbet.com/core}entityRef" minOccurs="0"/>
     *       &lt;/sequence>
     *       &lt;attribute name="timeStamp" type="{http://www.w3.org/2001/XMLSchema}dateTime" />
     *       &lt;attribute name="amount" type="{http://www.w3.org/2001/XMLSchema}decimal" />
     *     &lt;/restriction>
     *   &lt;/complexContent>
     * &lt;/complexType>
     * </pre>
     * 
     * 
     */
    @XmlAccessorType(XmlAccessType.FIELD)
    @XmlType(name = "", propOrder = {
        "shopRef",
        "operatorRef"
    })
    public static class SlipCollection
        implements Serializable
    {

        private final static long serialVersionUID = 1L;
        protected EntityRef shopRef;
        protected EntityRef operatorRef;
        @XmlAttribute
        @XmlSchemaType(name = "dateTime")
        protected XMLGregorianCalendar timeStamp;
        @XmlAttribute
        protected BigDecimal amount;
        @XmlAnyAttribute
        private Map<QName, String> otherAttributes = new HashMap<QName, String>();

        /**
         * Gets the value of the shopRef property.
         * 
         * @return
         *     possible object is
         *     {@link EntityRef }
         *     
         */
        public EntityRef getShopRef() {
            return shopRef;
        }

        /**
         * Sets the value of the shopRef property.
         * 
         * @param value
         *     allowed object is
         *     {@link EntityRef }
         *     
         */
        public void setShopRef(EntityRef value) {
            this.shopRef = value;
        }

        public boolean isSetShopRef() {
            return (this.shopRef!= null);
        }

        /**
         * Gets the value of the operatorRef property.
         * 
         * @return
         *     possible object is
         *     {@link EntityRef }
         *     
         */
        public EntityRef getOperatorRef() {
            return operatorRef;
        }

        /**
         * Sets the value of the operatorRef property.
         * 
         * @param value
         *     allowed object is
         *     {@link EntityRef }
         *     
         */
        public void setOperatorRef(EntityRef value) {
            this.operatorRef = value;
        }

        public boolean isSetOperatorRef() {
            return (this.operatorRef!= null);
        }

        /**
         * Gets the value of the timeStamp property.
         * 
         * @return
         *     possible object is
         *     {@link XMLGregorianCalendar }
         *     
         */
        public XMLGregorianCalendar getTimeStamp() {
            return timeStamp;
        }

        /**
         * Sets the value of the timeStamp property.
         * 
         * @param value
         *     allowed object is
         *     {@link XMLGregorianCalendar }
         *     
         */
        public void setTimeStamp(XMLGregorianCalendar value) {
            this.timeStamp = value;
        }

        public boolean isSetTimeStamp() {
            return (this.timeStamp!= null);
        }

        /**
         * Gets the value of the amount property.
         * 
         * @return
         *     possible object is
         *     {@link BigDecimal }
         *     
         */
        public BigDecimal getAmount() {
            return amount;
        }

        /**
         * Sets the value of the amount property.
         * 
         * @param value
         *     allowed object is
         *     {@link BigDecimal }
         *     
         */
        public void setAmount(BigDecimal value) {
            this.amount = value;
        }

        public boolean isSetAmount() {
            return (this.amount!= null);
        }

        /**
         * Gets a map that contains attributes that aren't bound to any typed property on this class.
         * 
         * <p>
         * the map is keyed by the name of the attribute and 
         * the value is the string value of the attribute.
         * 
         * the map returned by this method is live, and you can add new attribute
         * by updating the map directly. Because of this design, there's no setter.
         * 
         * 
         * @return
         *     always non-null
         */
        public Map<QName, String> getOtherAttributes() {
            return otherAttributes;
        }

    }

}
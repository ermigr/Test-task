'use strict';
const API='https://raw.githubusercontent.com/GeekBrainsTutorial/online-store-api/master/responses';


class List{
	constructor(url, container, list=list2){
		this.url=url;
		this.container=container;
		this.list=list;
		this.goods=[];
		this.allProducts=[];
		this.init();
	}

	getJson(url){
		return fetch(url? url:`${API+this.url}`)
					.then(data=>data.json())
					.catch(error=>alert(error))
	}

	render (){
		let block=document.querySelector(this.container);
		this.goods.forEach((product)=>{
			const object=new this.list[this.constructor.name](product);
			this.allProducts.push(object);
			block.insertAdjacentHTML('afterbegin',object.render());
		})
	}

	init(){
		false;
	}
}


class Item{
	constructor(el,img='https://via.placeholder.com/200x150'){
		this.id=el.id_product;
		this.name=el.product_name;
		this.price=el.price;
		this.img=img;
	}

	render(){
		return `<div class='product-item product-item-${this.id}'>
				<img src=${this.img}>
				<h2>${this.name}</h2>
				<p>${this.price}</p>
				<button class='btn-buy' data-id='${this.id}'>Купить</button>
				</div>`;
	}
}


class ProductList extends List{
	constructor(cart, url='/catalogData.json', container='.products'){
		super(url,container);
		this.cart=cart;
		this.getJson()
			.then(data=>{
				this.goods=[...data];
				this.render();
			})
	}

	filtered(text){
		let regexp=new RegExp(text.value,'i');
		this.allProducts.forEach(item=>{
			if (regexp.test(item.name)){
				document.querySelector(`.product-item-${item.id}`).classList.remove('invisible');
			} else {
				document.querySelector(`.product-item-${item.id}`).classList.add('invisible');
			}
		})
	}

	init(){
		const block=document.querySelector(this.container);
		block.addEventListener('click',e=>{
			if (e.target.classList.contains('btn-buy')){
				this.cart.addCart(e.target);
			}
		})
		const search=document.querySelector('.btn-search');
		const text=document.querySelector('input');
		search.addEventListener('click',()=>this.filtered(text));
	}
}


class ProductItem extends Item{}


class Cart extends List{
	constructor(url='/getBasket.json', container='.cart'){
		super(url,container);
		this.emptyCart();
	}

	addCart(el){
		let index=el.dataset['id'];
		let product=this.allProducts.find(item=>item.id==index) 
		if (product) {
			product.quantity++;
			this.updateCart(product);
		} else {	
			this.getJson()
				.then(data=>{
					this.goods=[...data.contents];
					this.goods=[this.goods.find(item=>item.id_product==index)];
					this.render();
					this.emptyCart();
				})
		}
	}

	removeCart(el){
		let id=el.dataset['id'];
		let product=this.allProducts.find(item=>item.id==id)
		if (product.quantity>1) {
			product.quantity--;
			this.updateCart(product);
		} else {
		document.querySelector(`.cart-item-${id}`).remove();
		this.allProducts=this.allProducts.filter(item=>item.id!=id);
		this.emptyCart();
		}
	}

	init(){
		const block=document.querySelector(this.container);
		block.addEventListener('click',e=>{
			if (e.target.classList.contains('btn-remove')){
				this.removeCart(e.target);
			}
		});
		const cart=document.querySelector('.btn-cart');
		cart.addEventListener('click',()=>block.classList.toggle('invisible'));
	}

	updateCart (product) {
		let block=document.querySelector(`.cart-item-${product.id}`);
		block.querySelector('.price').textContent=`Общая стоимость: ${product.quantity*product.price}`;
		block.querySelector('.quantity').textContent=`Количество: ${product.quantity}`;
	}

	emptyCart(){
		let ad=document.querySelector('.cart-empty');
		if (this.allProducts.reduce((sum,item)=>sum+=item.quantity,0)==0){
			ad.textContent='Корзина пуста';
		} 	else {
			ad.textContent='';
		}	
	}
}


class CartItem extends Item{
	constructor(el,img='https://via.placeholder.com/50x40'){
		super(el,img);
		this.quantity=1;
	}

	render(){
		return `<div class='cart-item cart-item-${this.id}'>
				<div class='cart-item-name cart-item-name-${this.id}'>
				<img src=${this.img}>
				<h2>${this.name}</h2>
				<p>${this.price}</p>
				</div>
				<div class='cart-item-sum cart-item-sum-${this.id}'>
				<p class='price'>Общая стоимость: ${this.quantity*this.price}</p>
				<p class='quantity'>Количество: ${this.quantity}</p>
				<button class=btn-remove data-id='${this.id}'>&times;</button>
				</div>
				</div>`;
	}
}

const list2={
	ProductList:ProductItem,
	Cart:CartItem
}

let cart=new Cart();
let productList=new ProductList(cart);
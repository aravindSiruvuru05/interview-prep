package main

type Bevarage interface {
	getPrice() int
}

type Coffee struct {
	price int
}

func (c *Coffee) getPrice() int {
	return c.price
}

func NewCoffee() Bevarage {
	return &Coffee{
		price: 10,
	}
}

type Mocha struct {
	b     Bevarage
	price int
}

func (m *Mocha) getPrice() int {
	return m.price + m.b.getPrice()
}

type Cardamom struct {
	b     Bevarage
	price int
}

func (c *Cardamom) getPrice() int {
	return c.price + c.b.getPrice()
}

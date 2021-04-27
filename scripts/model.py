import uuid
import numpy as np
from numpy.random import default_rng

from mesa import Agent, Model
from mesa.datacollection import DataCollector

from scheduler import RandomActivationByBreed
from model_data_collection import compute_gini


class Consumidore(Agent):
    ''' An agent with fixed initial wealth.'''
    def __init__(self, unique_id, model, num_empresas, ingreso_inicial, impuesto_ingreso):
        super().__init__(unique_id, model)
        rng = default_rng()

        # Dotaciones iniciales
        # self.theta = 1 / num_empresas
        self.oferta_trabajo_inicial = np.round(rng.uniform(), 2)
        self.ingreso_inicial = ingreso_inicial
        self.oferta_trabajo_disponible = self.oferta_trabajo_inicial
        self.ingreso_total = self.ingreso_inicial
        self.ingreso_disponible = self.ingreso_inicial
        self.impuesto_ingreso = impuesto_ingreso
        self.consumo = 0
        self.max_consumo = self.consumo
        self.delta_cambio_consumo = 0
        self.factor_descanso = np.round(rng.uniform(), 2)
        self.delta_oferta_trabajo = np.round(rng.uniform(0, 1 - self.oferta_trabajo_disponible), 2)
        # Temporal
        self.demanda_trabajo_disponible = np.round(rng.uniform(0, 5), 2)

    def cambio_oferta_trabajo(self):
        camaradas = self.model.schedule.agents

        if len(camaradas) > 1:
            otre = self.random.choice(camaradas)

            if (otre.delta_oferta_trabajo + self.oferta_trabajo_disponible) <= 1:
                self.delta_oferta_trabajo = otre.delta_oferta_trabajo
    
    def vive(self):
        self.ingreso_disponible -= self.model.costo_vida
    
    def jubila(self):
        self.model.schedule.remove(self)

    # Considerar la reprodución (que equivaldrá a que alguien ingresa al mercado laboral)

    def trabaja(self):
        camaradas = self.model.schedule.agents
        
        for i in range(len(camaradas)):
            otre = camaradas[i]
            oferta = self.oferta_trabajo_disponible
    
            if self.oferta_trabajo_disponible > 0 and otre.demanda_trabajo_disponible > 0:
                oferta = np.round(default_rng().uniform(0, self.oferta_trabajo_disponible), 2)

            salario = default_rng().integers(self.model.costo_vida, 400) * oferta
            self.oferta_trabajo_disponible -= oferta
            self.ingreso_disponible += salario
            self.ingreso_total += salario
            otre.demanda_trabajo_disponible -= oferta

    def paga_impuestos(self):
        camaradas = self.model.schedule.agents
        impuesto = self.impuesto_ingreso * self.ingreso_disponible
        
        for i in range(len(camaradas)):
            otre = camaradas[i]
            otre.ingreso_disponible += impuesto / len(camaradas)
    
    def consume(self):
        if self.ingreso_disponible > self.model.costo_vida:
            placeres = self.ingreso_disponible - self.model.costo_vida
            self.consumo = placeres

            if (self.consumo > self.max_consumo and self.max_consumo != 0):
                self.delta_cambio_consumo = (self.consumo / self.max_consumo) - 1
                self.max_consumo = self.consumo
            
            self.ingreso_disponible -= placeres
    
    def descansa(self):
        self.oferta_trabajo_disponible = self.factor_descanso * self.oferta_trabajo_disponible
        # Parto del supuesto donde, a mayor consumo, mayor bienestar, y a mayor bienestar, mayor eficiencia laboral. Por tanto, defino el factor consumo como: 
        self.factor_descanso = np.round(default_rng().uniform(0, self.delta_cambio_consumo), 2)
        # Temporal
        self.demanda_trabajo_disponible = np.round(default_rng().uniform(0, 5), 2)

    def step(self):
        # Si los ingresos del consumidore son menores a los costos de vivir, se jubila
        if self.ingreso_disponible < self.model.costo_vida:
            self.jubila()
        else:
            self.vive()
            self.trabaja()
            self.paga_impuestos()
            self.consume()
            self.descansa()

class Empresa(Agent):
    ''' An agent with fixed initial wealth.'''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        rng = default_rng()

        # Dotaciones iniciales
        self.demanda_trabajo = 0
        self.capital_inicial = np.round(rng.uniform(0, 5), 2)
        self.costo_capital = np.ro
        self.beneficios_totales = 0
        self.produccion = 0
        self.max_beneficios = 0
        self.costo_trabajo = 0
        self.costo_capital = np.round(rng.uniform(0, 5), 2)
        self.alfa = np.round(rng.uniform(), 2)
        self.num_trabajadores = 0


    def func_prod(self, trabajo, capital, alfa):
        return np.round((trabajo**alfa)*(capital**(1-alfa)), 2)

    def beneficios(self):
        # Normalizando los precios del bien a 1
        self.beneficios_totales = self.func_prod(self.demanda_trabajo, self.capital_inicial, self.alfa) 

    def produce(self):
        self.beneficios()

    def bancarrota(self):
        self.model.schedule.remove(self)

    def step(self):
        if self.beneficios < 0:
            self.bancarrota()
        
        self.produce()

class EconomiaSocialista(Model):
    '''A model with some number of agents.'''
    def __init__(self, I, J, impuesto_ingreso, costo_vida, ingreso_inicial):
        self.num_consumidores = I
        self.num_empresas = J
        self.schedule = RandomActivationByBreed(self)
        self.running = True
        self.impuesto_ingreso = impuesto_ingreso
        self.ingreso_inicial = ingreso_inicial
        self.costo_vida = costo_vida

        # Create agents
        for i in range(self.num_consumidores):
            a = Consumidore(uuid.uuid4(), self, self.num_empresas, self.ingreso_inicial, self.impuesto_ingreso)
            self.schedule.add(a)
        
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},  # `compute_gini` defined above
            agent_reporters={"Ingreso total": "ingreso_total"}
        )

    def entrada_mercado_laboral(self):
        nueves_consumidores = self.num_consumidores - len(self.schedule.agents)

        if nueves_consumidores != 0:
            for i in range(nueves_consumidores):
                a = Consumidore(uuid.uuid4(), self, self.num_empresas, self.ingreso_inicial, self.impuesto_ingreso)
                self.schedule.add(a)

    def step(self):
        '''Advance the model by one step.'''
        
        self.entrada_mercado_laboral()
        self.datacollector.collect(self)
        self.schedule.step(by_breed=False)

from beatadjoint import CardiacCellModel
from dolfin import *
from dolfin_adjoint import *

class Tentusscher_2004_mcell(CardiacCellModel):
    """
NOT_IMPLEMENTED    
    """
    def __init__(self, parameters=None):
        CardiacCellModel.__init__(self, parameters)

    def default_parameters(self):
        parameters = Parameters("Tentusscher_2004_mcell")
        parameters.add("P_kna", 0.03)
        parameters.add("g_K1", 5.405)
        parameters.add("g_Kr", 0.096)
        parameters.add("g_Ks", 0.062)
        parameters.add("g_Na", 14.838)
        parameters.add("g_bna", 0.00029)
        parameters.add("g_CaL", 0.000175)
        parameters.add("g_bca", 0.000592)
        parameters.add("g_to", 0.294)
        parameters.add("K_mNa", 40)
        parameters.add("K_mk", 1)
        parameters.add("P_NaK", 1.362)
        parameters.add("K_NaCa", 1000)
        parameters.add("K_sat", 0.1)
        parameters.add("Km_Ca", 1.38)
        parameters.add("Km_Nai", 87.5)
        parameters.add("alpha", 2.5)
        parameters.add("gamma", 0.35)
        parameters.add("K_pCa", 0.0005)
        parameters.add("g_pCa", 0.825)
        parameters.add("g_pK", 0.0146)
        parameters.add("Buf_c", 0.15)
        parameters.add("Buf_sr", 10)
        parameters.add("Ca_o", 2)
        parameters.add("K_buf_c", 0.001)
        parameters.add("K_buf_sr", 0.3)
        parameters.add("K_up", 0.00025)
        parameters.add("V_leak", 8e-05)
        parameters.add("V_sr", 0.001094)
        parameters.add("Vmax_up", 0.000425)
        parameters.add("a_rel", 0.016464)
        parameters.add("b_rel", 0.25)
        parameters.add("c_rel", 0.008232)
        parameters.add("tau_g", 2)
        parameters.add("Na_o", 140)
        parameters.add("Cm", 0.185)
        parameters.add("F", 96485.3415)
        parameters.add("R", 8314.472)
        parameters.add("T", 310)
        parameters.add("V_c", 0.016404)
        parameters.add("K_o", 5.4)
        return parameters

    def I(self, v, s):
        """
        Transmembrane current
        """
        # Imports
        # No imports for now

        # Assign states
        V = v
        states = split(s)
        assert(len(states) == 16)
        Xr1, Xr2, Xs, m, h, j, d, f, fCa, s, r, Ca_SR, Ca_i, g, Na_i, K_i =\
            states

        # Assign parameters
        g_bca = self._coefficient_parameters["g_bca"]
        g_CaL = self._coefficient_parameters["g_CaL"]
        K_o = self._coefficient_parameters["K_o"]
        Ca_o = self._coefficient_parameters["Ca_o"]
        g_pCa = self._coefficient_parameters["g_pCa"]
        g_Ks = self._coefficient_parameters["g_Ks"]
        g_Kr = self._coefficient_parameters["g_Kr"]
        P_kna = self._coefficient_parameters["P_kna"]
        K_pCa = self._coefficient_parameters["K_pCa"]
        P_NaK = self._coefficient_parameters["P_NaK"]
        Km_Nai = self._coefficient_parameters["Km_Nai"]
        g_to = self._coefficient_parameters["g_to"]
        K_mNa = self._coefficient_parameters["K_mNa"]
        F = self._coefficient_parameters["F"]
        g_bna = self._coefficient_parameters["g_bna"]
        Na_o = self._coefficient_parameters["Na_o"]
        R = self._coefficient_parameters["R"]
        T = self._coefficient_parameters["T"]
        alpha = self._coefficient_parameters["alpha"]
        K_sat = self._coefficient_parameters["K_sat"]
        K_NaCa = self._coefficient_parameters["K_NaCa"]
        g_pK = self._coefficient_parameters["g_pK"]
        g_K1 = self._coefficient_parameters["g_K1"]
        Km_Ca = self._coefficient_parameters["Km_Ca"]
        g_Na = self._coefficient_parameters["g_Na"]
        K_mk = self._coefficient_parameters["K_mk"]
        gamma = self._coefficient_parameters["gamma"]

        current = -1.0*Ca_i*g_pCa/(Ca_i + K_pCa) - 4.0*ufl.pow(F,\
            2.0)*T*V*d*f*fCa*g_CaL*(Ca_i*ufl.exp(2.0*F*T*V/R) -\
            0.341*Ca_o)/(R*(ufl.exp(2.0*F*T*V/R) - 1.0)) - 1.0*K_NaCa*(Ca_o +\
            Km_Ca)*(K_sat*ufl.exp(F*T*V*(gamma - 1.0)/R) +\
            1.0)*(-Ca_i*ufl.pow(Na_o, 3.0)*alpha*ufl.exp(F*T*V*(gamma -\
            1.0)/R) + Ca_o*ufl.pow(Na_i,\
            3.0)*ufl.exp(F*T*V*gamma/R))/(ufl.pow(Km_Nai, 3.0) +\
            ufl.pow(Na_o, 3.0)) -\
            0.430331482911935*ufl.sqrt(K_o)*Xr1*Xr2*g_Kr*(V -\
            R*T*ufl.ln(K_o/K_i)/F) - 0.0430331482911935*ufl.sqrt(K_o)*g_K1*(V\
            - R*T*ufl.ln(K_o/K_i)/F)/((0.1/(ufl.exp(0.06*V - 12.0 -\
            0.06*R*T*ufl.ln(K_o/K_i)/F) + 1.0) + (3.0*ufl.exp(0.0002*V + 0.02\
            - 0.0002*R*T*ufl.ln(K_o/K_i)/F) + ufl.exp(0.1*V - 1.0 -\
            0.1*R*T*ufl.ln(K_o/K_i)/F))/(ufl.exp(-0.5*V +\
            0.5*R*T*ufl.ln(K_o/K_i)/F) + 1.0))*(ufl.exp(0.06*V - 12.0 -\
            0.06*R*T*ufl.ln(K_o/K_i)/F) + 1.0)) - 1.0*K_o*Na_i*P_NaK/((K_mNa\
            + Na_i)*(K_mk + K_o)*(1.0 + 0.0353*ufl.exp(-F*T*V/R) +\
            0.1245*ufl.exp(-0.1*F*T*V/R))) - 1.0*ufl.pow(Xs, 2.0)*g_Ks*(V -\
            R*T*ufl.ln((K_o + Na_o*P_kna)/(K_i + Na_i*P_kna))/F) -\
            1.0*g_Na*h*j*ufl.pow(m, 3.0)*(V - R*T*ufl.ln(Na_o/Na_i)/F) -\
            1.0*g_bca*(V - 0.5*R*T*ufl.ln(Ca_o/Ca_i)/F) - 1.0*g_bna*(V -\
            R*T*ufl.ln(Na_o/Na_i)/F) - 1.0*g_pK*(V -\
            R*T*ufl.ln(K_o/K_i)/F)/(ufl.exp(-0.167224080267559*V +\
            4.18060200668896) + 1.0) - 1.0*g_to*r*s*(V -\
            R*T*ufl.ln(K_o/K_i)/F)

        
        return current

    def F(self, v, s):
        """
        Right hand side for ODE system
        """
        # Imports
        # No imports for now

        # Assign states
        V = v
        states = split(s)
        assert(len(states) == 16)
        Xr1, Xr2, Xs, m, h, j, d, f, fCa, s, r, Ca_SR, Ca_i, g, Na_i, K_i =\
            states

        # Assign parameters
        Buf_c = self._coefficient_parameters["Buf_c"]
        g_bca = self._coefficient_parameters["g_bca"]
        K_o = self._coefficient_parameters["K_o"]
        g_CaL = self._coefficient_parameters["g_CaL"]
        a_rel = self._coefficient_parameters["a_rel"]
        c_rel = self._coefficient_parameters["c_rel"]
        K_up = self._coefficient_parameters["K_up"]
        V_sr = self._coefficient_parameters["V_sr"]
        Ca_o = self._coefficient_parameters["Ca_o"]
        g_pCa = self._coefficient_parameters["g_pCa"]
        g_Ks = self._coefficient_parameters["g_Ks"]
        g_Kr = self._coefficient_parameters["g_Kr"]
        Vmax_up = self._coefficient_parameters["Vmax_up"]
        P_kna = self._coefficient_parameters["P_kna"]
        K_pCa = self._coefficient_parameters["K_pCa"]
        P_NaK = self._coefficient_parameters["P_NaK"]
        V_c = self._coefficient_parameters["V_c"]
        V_leak = self._coefficient_parameters["V_leak"]
        Km_Nai = self._coefficient_parameters["Km_Nai"]
        g_to = self._coefficient_parameters["g_to"]
        Buf_sr = self._coefficient_parameters["Buf_sr"]
        K_mNa = self._coefficient_parameters["K_mNa"]
        F = self._coefficient_parameters["F"]
        g_bna = self._coefficient_parameters["g_bna"]
        K_buf_sr = self._coefficient_parameters["K_buf_sr"]
        Na_o = self._coefficient_parameters["Na_o"]
        b_rel = self._coefficient_parameters["b_rel"]
        T = self._coefficient_parameters["T"]
        alpha = self._coefficient_parameters["alpha"]
        K_sat = self._coefficient_parameters["K_sat"]
        K_buf_c = self._coefficient_parameters["K_buf_c"]
        K_NaCa = self._coefficient_parameters["K_NaCa"]
        g_pK = self._coefficient_parameters["g_pK"]
        Cm = self._coefficient_parameters["Cm"]
        g_K1 = self._coefficient_parameters["g_K1"]
        Km_Ca = self._coefficient_parameters["Km_Ca"]
        R = self._coefficient_parameters["R"]
        g_Na = self._coefficient_parameters["g_Na"]
        tau_g = self._coefficient_parameters["tau_g"]
        K_mk = self._coefficient_parameters["K_mk"]
        gamma = self._coefficient_parameters["gamma"]

        F_expressions = [\

            0.00037037037037037*(-Xr1 + 1.0/(ufl.exp(-0.142857142857143*V -\
            3.71428571428571) + 1.0))*(ufl.exp(-0.1*V - 4.5) +\
            1.0)*(ufl.exp(0.0869565217391304*V + 2.60869565217391) + 1.0),

            0.297619047619048*(-Xr2 + 1.0/(ufl.exp(0.0416666666666667*V +\
            3.66666666666667) + 1.0))*(ufl.exp(-0.05*V - 3.0) +\
            1.0)*(ufl.exp(0.05*V - 3.0) + 1.0),

            0.000909090909090909*(-Xs + 1.0/(ufl.exp(-0.0714285714285714*V -\
            0.357142857142857) + 1.0))*ufl.sqrt(ufl.exp(-0.166666666666667*V\
            - 1.66666666666667) + 1.0)*(ufl.exp(0.05*V - 3.0) + 1.0),

            1.0*(-m + 1.0*ufl.pow(ufl.exp(-0.110741971207087*V -\
            6.29678848283499) + 1.0, -2.0))*(ufl.exp(-0.2*V - 12.0) +\
            1.0)/(0.1/(ufl.exp(0.2*V + 7.0) + 1.0) + 0.1/(ufl.exp(0.005*V -\
            0.25) + 1.0)),

            (-h + 1.0*ufl.pow(ufl.exp(0.134589502018843*V + 9.62987886944818)\
            + 1.0, -2.0))*(1.0*(0.057 - 0.057/(ufl.exp(1.0*V + 40.0) +\
            1.0))*ufl.exp(-0.147058823529412*V - 11.7647058823529) + 1.0*(1.0\
            - 1.0/(ufl.exp(1.0*V + 40.0) + 1.0))*(2.7*ufl.exp(0.079*V) +\
            310000.0*ufl.exp(0.3485*V)) +\
            1.0*(5.92307692307692*ufl.exp(-0.0900900900900901*V -\
            0.96036036036036) + 5.92307692307692)/(ufl.exp(1.0*V + 40.0) +\
            1.0)),

            (-j + 1.0*ufl.pow(ufl.exp(0.134589502018843*V + 9.62987886944818)\
            + 1.0, -2.0))*(1.0*(0.02424 - 0.02424/(ufl.exp(1.0*V + 40.0) +\
            1.0))*ufl.exp(-0.01052*V)/(ufl.exp(-0.1378*V - 5.531292) + 1.0) +\
            1.0*(1.0 - 1.0/(ufl.exp(1.0*V + 40.0) + 1.0))*(V +\
            37.78)*(-25428.0*ufl.exp(0.2444*V) -\
            6.948*ufl.exp(-0.04391*V))/(ufl.exp(0.311*V + 24.64053) + 1.0) +\
            0.6*ufl.exp(0.057*V)/((ufl.exp(-0.1*V - 3.2) +\
            1.0)*(ufl.exp(1.0*V + 40.0) + 1.0))),

            (-d + 1.0/(ufl.exp(-0.133333333333333*V - 0.666666666666667) +\
            1.0))/(1.4*(0.25 + 1.4/(ufl.exp(-0.0769230769230769*V -\
            2.69230769230769) + 1.0))/(ufl.exp(0.2*V + 1.0) + 1.0) +\
            1.0/(ufl.exp(-0.05*V + 2.5) + 1.0)),

            (-f + 1.0/(ufl.exp(0.142857142857143*V + 2.85714285714286) +\
            1.0))/(80.0 + 1125.0*ufl.exp(-0.00416666666666667*ufl.pow(V +\
            27.0, 2.0)) + 165.0/(ufl.exp(-0.1*V + 2.5) + 1.0)),

            (-0.5*fCa + 0.078767123287671 +\
            0.0342465753424658/(ufl.exp(10000.0*Ca_i - 5.0) + 1.0) +\
            0.0684931506849315/(ufl.exp(1250.0*Ca_i - 0.9375) + 1.0) +\
            0.342465753424658/(ufl.pow(3076.92307692308*Ca_i, 8.0) +\
            1.0))/(ufl.exp(-1.0*V - 60.0) + 1.0),

            (-s + 1.0/(ufl.exp(0.2*V + 4.0) + 1.0))/(3.0 +\
            85.0*ufl.exp(-0.003125*ufl.pow(V + 45.0, 2.0)) +\
            5.0/(ufl.exp(0.2*V - 4.0) + 1.0)),

            (-r + 1.0/(ufl.exp(-0.166666666666667*V + 3.33333333333333) +\
            1.0))/(0.8 + 9.5*ufl.exp(-0.000555555555555556*ufl.pow(V + 40.0,\
            2.0))),

            1.0*V_c*(-V_leak*(Ca_SR - Ca_i) + Vmax_up/(ufl.pow(Ca_i,\
            -2.0)*ufl.pow(K_up, 2.0) + 1.0) - d*g*(ufl.pow(Ca_SR,\
            2.0)*a_rel/(ufl.pow(Ca_SR, 2.0) + ufl.pow(b_rel, 2.0)) +\
            c_rel))/(V_sr*(Buf_sr*K_buf_sr*ufl.pow(Ca_SR + K_buf_sr, -2.0) +\
            1.0)),

            1.0*(-Cm*F*V_c*(0.5*Ca_i*g_pCa/(Ca_i + K_pCa) + 2.0*ufl.pow(F,\
            2.0)*T*V*d*f*fCa*g_CaL*(Ca_i*ufl.exp(2.0*F*T*V/R) -\
            0.341*Ca_o)/(R*(ufl.exp(2.0*F*T*V/R) - 1.0)) - 1.0*K_NaCa*(Ca_o +\
            Km_Ca)*(K_sat*ufl.exp(F*T*V*(gamma - 1.0)/R) +\
            1.0)*(-Ca_i*ufl.pow(Na_o, 3.0)*alpha*ufl.exp(F*T*V*(gamma -\
            1.0)/R) + Ca_o*ufl.pow(Na_i,\
            3.0)*ufl.exp(F*T*V*gamma/R))/(ufl.pow(Km_Nai, 3.0) +\
            ufl.pow(Na_o, 3.0)) + 0.5*g_bca*(V -\
            0.5*R*T*ufl.ln(Ca_o/Ca_i)/F)) + V_leak*(Ca_SR - Ca_i) -\
            Vmax_up/(ufl.pow(Ca_i, -2.0)*ufl.pow(K_up, 2.0) + 1.0) +\
            d*g*(ufl.pow(Ca_SR, 2.0)*a_rel/(ufl.pow(Ca_SR, 2.0) +\
            ufl.pow(b_rel, 2.0)) + c_rel))/(Buf_c*K_buf_c*ufl.pow(Ca_i +\
            K_buf_c, -2.0) + 1.0),

            (-g + (1.0 - 1.0/(ufl.exp(1.0*Ca_i - 0.00035) +\
            1.0))/(ufl.pow(2857.14285714286*Ca_i, 6.0) + 1.0) +\
            1.0/((ufl.pow(2857.14285714286*Ca_i, 16.0) +\
            1.0)*(ufl.exp(1.0*Ca_i - 0.00035) + 1.0)))/(tau_g*(ufl.exp(-1.0*V\
            - 60.0) + 1.0)),

            1.0*Cm*F*V_c*(-3.0*K_NaCa*(Ca_o +\
            Km_Ca)*(K_sat*ufl.exp(F*T*V*(gamma - 1.0)/R) +\
            1.0)*(-Ca_i*ufl.pow(Na_o, 3.0)*alpha*ufl.exp(F*T*V*(gamma -\
            1.0)/R) + Ca_o*ufl.pow(Na_i,\
            3.0)*ufl.exp(F*T*V*gamma/R))/(ufl.pow(Km_Nai, 3.0) +\
            ufl.pow(Na_o, 3.0)) - 3.0*K_o*Na_i*P_NaK/((K_mNa + Na_i)*(K_mk +\
            K_o)*(1.0 + 0.0353*ufl.exp(-F*T*V/R) +\
            0.1245*ufl.exp(-0.1*F*T*V/R))) - 1.0*g_Na*h*j*ufl.pow(m, 3.0)*(V\
            - R*T*ufl.ln(Na_o/Na_i)/F) - 1.0*g_bna*(V -\
            R*T*ufl.ln(Na_o/Na_i)/F)),

            1.0*Cm*F*V_c*(-0.430331482911935*ufl.sqrt(K_o)*Xr1*Xr2*g_Kr*(V -\
            R*T*ufl.ln(K_o/K_i)/F) - 0.0430331482911935*ufl.sqrt(K_o)*g_K1*(V\
            - R*T*ufl.ln(K_o/K_i)/F)/((0.1/(ufl.exp(0.06*V - 12.0 -\
            0.06*R*T*ufl.ln(K_o/K_i)/F) + 1.0) + (3.0*ufl.exp(0.0002*V + 0.02\
            - 0.0002*R*T*ufl.ln(K_o/K_i)/F) + ufl.exp(0.1*V - 1.0 -\
            0.1*R*T*ufl.ln(K_o/K_i)/F))/(ufl.exp(-0.5*V +\
            0.5*R*T*ufl.ln(K_o/K_i)/F) + 1.0))*(ufl.exp(0.06*V - 12.0 -\
            0.06*R*T*ufl.ln(K_o/K_i)/F) + 1.0)) + 2.0*K_o*Na_i*P_NaK/((K_mNa\
            + Na_i)*(K_mk + K_o)*(1.0 + 0.0353*ufl.exp(-F*T*V/R) +\
            0.1245*ufl.exp(-0.1*F*T*V/R))) - 1.0*ufl.pow(Xs, 2.0)*g_Ks*(V -\
            R*T*ufl.ln((K_o + Na_o*P_kna)/(K_i + Na_i*P_kna))/F) -\
            1.0*g_pK*(V -\
            R*T*ufl.ln(K_o/K_i)/F)/(ufl.exp(-0.167224080267559*V +\
            4.18060200668896) + 1.0) - 1.0*g_to*r*s*(V -\
            R*T*ufl.ln(K_o/K_i)/F)),
            ]

        return as_vector(F_expressions)

    def initial_conditions(self):
        ic = Expression(["V", "Xr1", "Xr2", "Xs", "m", "h", "j", "d", "f",\
            "fCa", "s", "r", "Ca_SR", "Ca_i", "g", "Na_i", "K_i"],\
            V=-86.2, Xr1 = 0, Xr2 = 1, Xs = 0, m = 0, h = 0.75, j = 0.75, d =\
            0, f = 1, fCa = 1, s = 1, r = 0, Ca_SR = 0.2, Ca_i = 0.0002, g =\
            1, Na_i = 11.6, K_i = 138.3)

        return ic

    def num_states(self):
        return 16

    def __str__(self):
        return 'Tentusscher_2004_mcell cardiac cell model'
from django.views import View
from django.shortcuts import render
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import math
from plotly.io import to_html
from numpy import cos
from numpy import e
from numpy import linspace
from numpy import pi
from numpy import sin
from numpy import tan
from sympy import symbols, sympify, lambdify
from sympy.utilities.autowrap import ufuncify

class TrapesiumView(View):
    context = {"error": "", "hasil": "", "a": "", "b": "", "fx": "", "n": "", "delta_x": "", "fig": ""}
    template_file = 'trapesium.html'

    def get(self, request):
        return render(request, self.template_file, self.context)

    def post(self, request):
        try:
            a = request.POST.get("a")
            b = request.POST.get("b")
            fx = request.POST.get("fx")
            self.context.update({"a": a, "b": b, "fx": fx})

            if request.POST.get("n") and not request.POST.get("delta_x"):
                n = eval(request.POST.get("n"))
                self.context["n"] = n
                
                e_symbol = symbols("e")
                pi_symbol = symbols("pi")
                f = sympify(fx)
                fx_sym = f.subs(e_symbol, e).subs(pi_symbol, pi)
                
                self.integral_trapesium_n(eval(a), eval(b), n, fx_sym)

            elif request.POST.get("delta_x") and not request.POST.get("n"):
                delta_x = eval(request.POST.get("delta_x"))
                self.context["delta_x"] = delta_x
                
                e_symbol = symbols("e")
                pi_symbol = symbols("pi")
                f = sympify(fx)
                fx_sym = f.subs(e_symbol, e).subs(pi_symbol, pi)
                
                self.integral_trapesium_delta_x(eval(a), eval(b), delta_x, fx_sym)

            else:
                self.context["hasil"] = "Invalid input"
        
        except Exception as err:
            self.context["hasil"] = f"Error: {str(err)}"

        return render(request, 'trapesium.html', self.context)


    def integral_trapesium_n(self, a, b, n, fx, graph=True):
        # menghitung nilai integral numerik
        def f(x):
            return fx.subs(symbols("x"), x)
        
        delta_x = (b - a)/(n)
        print(f"{delta_x=}")
        x_hitung = linspace(a,b,n+1)
        
        jumlah =  f(a) + f(b)
        for i in range(1, n):
            print(f"loopp ==== {i=}")
            print(f"loopp ==== {x_hitung[i]=}")
            print(f"loopp ==== {f(x_hitung[i])=}")
            jumlah += 2 * f(x_hitung[i])

        print(jumlah)

        hasil = (delta_x/2) * jumlah
        print(hasil)
        self.context["hasil"] = hasil

        # menghitung nilai error
        int_real = self.calc_real_integral(a, b, fx)
        error = self.calc_error(int_real, hasil)
        self.context["error"] = error

        # menggambar graf
        if graph:
            y_hitung = lambdify("x", fx, modules=["numpy"])(x_hitung)
            x_real = linspace(a,b,100)
            x_real_padding = linspace(a-1,b+1,100)
            y_real = lambdify("x", fx, modules=["numpy"])(x_real)
            y_real_padding = lambdify("x", fx, modules=["numpy"])(x_real_padding)
            print(y_real)
            df = pd.DataFrame({'x': x_real, 'y': y_real})
            fig = px.line(df, x='x', y='y')
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=x_hitung,
                    y=y_hitung,
                    fill="tozeroy",
                    name="nilai hitung",
                    line=dict(color='red')
                ),
            )

            fig.add_trace(
                go.Line(
                    x=x_real_padding,
                    y=y_real_padding,
                    showlegend=False,
                    name="nilai asli",
                    line=dict(color="deepskyblue"),
                )
            )

            for i in range(0, len(x_hitung)):
                fig.add_trace(go.Scatter(
                    x=[x_hitung[i], x_hitung[i]],
                    y=[0, y_hitung[i]],
                    mode='lines',
                    line=dict(color='red'),
                    showlegend=False
                ))

            fig.add_trace(
                go.Line(
                    x=x_real,
                    y=y_real,
                    name="nilai asli",
                    line=dict(color="deepskyblue"),
                    fill="tozeroy"
                )
            )


            self.context["fig"] = to_html(fig, full_html=False, default_width="50%", 
                        include_plotlyjs="cdn", div_id="ohlc")



    def integral_trapesium_delta_x(self, a, b, delta_x, fx, graph=True):
        # menghitung nilai integral numerik
        def f(x):
            return fx.subs(symbols("x"), x)
        
        n = math.ceil((b - a)/(delta_x))+1
        x_hitung = linspace(a,b,n)
        
        jumlah =  f(a) + f(b)
        for i in range(1, n-1):
            jumlah += 2 * f(x_hitung[i])

        print(jumlah)

        hasil = (delta_x/2) * jumlah

        self.context["hasil"] = hasil

        # menghitung nilai error
        int_real = self.calc_real_integral(a, b, fx)
        print(f"{ int_real= }")
        error = self.calc_error(int_real, hasil)
        self.context["error"] = error

        # menggambar graf
        if graph:
            y_hitung = lambdify("x", fx, modules=["numpy"])(x_hitung)
            x_real = linspace(a,b,100)
            x_real_padding = linspace(a-1,b+1,100)
            y_real = lambdify("x", fx, modules=["numpy"])(x_real)
            y_real_padding = lambdify("x", fx, modules=["numpy"])(x_real_padding)
            print(y_real)
            df = pd.DataFrame({'x': x_real, 'y': y_real})
            fig = px.line(df, x='x', y='y')
            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=x_hitung,
                    y=y_hitung,
                    fill="tozeroy",
                    name="nilai hitung",
                    line=dict(color='red')
                ),
            )

            fig.add_trace(
                go.Line(
                    x=x_real_padding,
                    y=y_real_padding,
                    showlegend=False,
                    name="nilai asli",
                    line=dict(color="deepskyblue"),
                )
            )

            for i in range(0, len(x_hitung)):
                fig.add_trace(go.Scatter(
                    x=[x_hitung[i], x_hitung[i]],
                    y=[0, y_hitung[i]],
                    mode='lines',
                    line=dict(color='red'),
                    showlegend=False
                ))

            fig.add_trace(
                go.Line(
                    x=x_real,
                    y=y_real,
                    name="nilai asli",
                    line=dict(color="deepskyblue"),
                    fill="tozeroy"
                )
            )


            self.context["fig"] = to_html(fig, full_html=False, default_width="50%", 
                        include_plotlyjs="cdn", div_id="ohlc")


    def calc_real_integral(self, a,b,fx):
        def f(x):
            return fx.subs(symbols("x"), x)
        return f(b) - f(a)

    def calc_error(self, real, calculated):
        return f"{((real-calculated)/real) * 100}%"
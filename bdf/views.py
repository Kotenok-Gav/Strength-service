from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from decimal import Decimal

from bdf.models import Rockets_bdf
from .forms import Rockets_bdfForm


def index(request):
    # домашня страница приложения bdf
    return render(request, 'bdf/index.html')


@login_required()
def rockets_bdf_all(request):
    # выводит все проекты
    rockets_bdf_all = Rockets_bdf.objects.filter(owner=request.user).all()
    context = {'rockets_bdf_all': rockets_bdf_all}
    return render(request, 'bdf/rockets_bdf_all.html', context)


@login_required()
def rocket(request, rocket_id):
    # выводит один проект
    rocket = Rockets_bdf.objects.get(id=rocket_id)
    #проверка того что тема принадлежит текущему пользователю
    if rocket.owner != request.user:
        raise Http404
    context = {"rocket": rocket}
    return render(request, 'bdf/rocket.html', context)


@login_required()
def rocket_bdf_new(request):
    #Создаем новый проект
    if request.method != 'POST':
        #Данные не отправляются, создается пустая форма
        form = Rockets_bdfForm
    else:
        #Отправлены данные POST, форма заполняется
        form = Rockets_bdfForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            file = open("1.txt", "w")
            file.write("NASTRAN SYSTEM(151)=1\nNASTRAN BUFFSIZE=65537\n\nID START\nTIME	300\nSOL	129\nDIAG	8,50\nCEND\necho=both\n\n")
            file.write("DISPLACEMENT(SORT1,REAL)	= all\nSPCFORCES(SORT1, REAL) = all\nFORCE(SORT1, REAL, BILIN) = all\n")
            file.write("VELOCITY = all\nACCELERATION = all\nOLOAD(SORT1, REAL) = all\nLOADSET = 100\n\nSUBCASE 1\nSUBTITLE = STATIKA\n")
            file.write("DISPLACEMENT = ALL\nLOAD = 222\nSPC = 10\nTSTEPNL = 1\nPARAM, TSTATIC, 1\n\n")
            file.write("SUBCASE 2\nSUBTITLE =   DINAMIKA_1\nPARAM,TSTATIC,-1\nDLOAD=210\nDISPLACEMENT=ALL\n")
            file.write("TSTEPNL=2\nNONLINEAR=1\nSPC=10\nSTATSUB  =   5\n\n")
            file.write("OUTPUT(XYPLOT)\n   PLOTTER = NAST\n   CSCALE = 1.3\n   XAXIS = YES\n   YAXIS = YES\n")
            file.write("   XTITLE = TIME IN SEC\n   YTITLE = DISPLACEMENT\nXYPLOT DISP RESP / 11(T2) / 11(T3) / 11(R1)\n")
            file.write("BEGIN   BULK\nPARAM   G           0.1\nPARAM   W3          1.0\n\nPARAM   POST      0\n")
            file.write("PARAM   PRTMAXIM  YES\n\n")
#            file.write(str(new_topic.start_rocket))

            # Запись GRID с 1 по N-й узел
            u = 0
            k = 0.1
            while u < new_topic.N:
                cox = u * k
                u += 1
                file.write("GRID    {: <8d}        {: <8.1f}\n".format(u, cox))
            file.write("\n")

            # Запись GRID с 100001 по 10000N-й узел контейнера
            u = 0
            k = 0.1
            d0 = 0
            while u < new_topic.N:
                u_1 = 100001 + u
                cox = u * k
                coy = (d0 / 2) + 0.1
                u += 1
                file.write("GRID    {: <8d}        {: <8.1f}{: <8.2f}\n".format(u_1, cox, coy))
            file.write("\n")

            # Запись GRID для баков окилителя с Xo+1000 по (Xo+o)+1000 узел
            k = Decimal('0.1')
            o = ((new_topic.Xo + new_topic.Lo) / k + 1001)
            o1 = (new_topic.Xo / k + 1001)
            u = o1
            while u < o + 1:
                cox = (u - 1001) * k
                u += 1
                u = int(u)
                file.write("GRID    {: <8d}        {: <8.1f}\n".format(u, cox))
            file.write("\n")

            # Запись GRID для баков горючего с Xg+1000 по (Xg+g)+1000 узел
            g = ((new_topic.Xg + new_topic.Lg) / k + 1001)
            g1 = (new_topic.Xg / k + 1001)
            u = g1
            while u < g + 1:
                cox = (u - 1001) * k
                u += 1
                u = int(u)
                file.write("GRID    {: <8d}        {: <8.1f}\n".format(u, cox))
            file.write("\n\n")

            # Запись CBAR с 1 по N-1-й узел
            u = 0
            Np = 1  # Np - номер параметра балочного элемента (для ракеты =1 )
            while u < new_topic.N:
                u += 1
                u = int(u)
                file.write("CBAR    {: <8d}{: <8d}{: <8d}{: <8d}0.0     1.0     0.0\n".format(u, Np, u, u + 1))
            file.write("\n\n")

            # Запись CBAR с 100001 по 10000N-1-й узел контейнера
            u = 0
            Np = 2  # Np - номер параметра балочного элемента (для контейнера =2 )
            while u < new_topic.N + 10:
                u += 1
                u = int(u)
                file.write(
                    "CBAR    {: <8d}{: <8d}{: <8d}{: <8d}0.0     1.0     0.0\n".format(u + 100000, Np, u + 100000, u + 100001))
            file.write("\n\n")

            # Запись RDE2 для баков окислителя с Xo+1000 по (Xo+o)+1000 узел
            u = o1
            while u < o + 1:
                u += 1
                u = int(u)
                file.write("RBE2    {: <8d}{: <8d}2       {: <8d}\n".format(u + 1000, u - 1000, u))
            file.write("\n")
            file.write("RBE2    {: <8.1f}{: <8.1f}1       {: <8.1f}\n".format(o1 + 2000, o1 - 1000, o1))
            u = o1
            while u < o:
                u += 1
                u = int(u)
                file.write("RBE2    {: <8d}{: <8d}1       {: <8d}\n".format(u + 2001, u, u + 1))
            file.write("\n")

            # Запись RDE2 для баков горючего с Xg+1000 по (Xg+g)+1000 узел
            u = g1
            while u < g + 1:
                u += 1
                u = int(u)
                file.write("RBE2    {: <8d}{: <8d}2       {: <8d}\n".format(u + 1000, u - 1000, u))
            file.write("\n\n")
            file.write("RBE2    {: <8.1f}{: <8.1f}1       {: <8.1f}\n".format(g1 + 2000, g1 - 2000, g1))
            u = g1
            while u < g:
                u += 1
                u = int(u)
                file.write("RBE2    {: <8d}{: <8d}1       {: <8d}\n".format(u + 2001, u, u + 1))
            file.write("\n\n")

            # Запись CONM2 для бака окислителя
            mo_uzla = new_topic.mo / (o - o1)  # определение сосредоточенной массы узла бака окислителя
            u = o1
            while u < o + 1:
                u += 1
                u = int(u)
                file.write("CONM2   {: <8d}{: <8d}        {: <8.1f}\n".format(u, u, mo_uzla))
            file.write("\n")

            # Запись CONM2 для бака горючего
            mg_uzla = new_topic.mg / (g - g1)  # определение сосредоточенной массы узла бака горючего
            u = g1
            while u < g + 1:
                u += 1
                u = int(u)
                file.write("CONM2   {: <8d}{: <8d}        {: <8.1f}\n".format(u, u, mg_uzla))
            file.write("\n")

            # Запись CONM2 сосредоточенных масс (ду,су,пн)
            if (new_topic.m_dy > 0):
                n_dy = ((new_topic.X_dy / k) + 1)
                file.write("CONM2   {: <8.1f}{: <8.1f}        {: <8.2f}\n".format(n_dy + 7000, n_dy, new_topic.m_dy))
            if (new_topic.m_cy > 0):
                n_cy = ((new_topic.X_cy / k) + 1)
                file.write("CONM2   {: <8.1f}{: <8.1f}        {: <8.2f}\n".format(n_cy + 7000, n_cy, new_topic.m_cy))
            if (new_topic.m_gch > 0):
                n_gch = ((new_topic.X_gch / k) + 1)
                file.write("CONM2   {: <8.1f}{: <8.1f}        {: <8.2f}\n".format(n_gch + 7000, n_gch, new_topic.m_gch))
            file.write("\n")

            # Запись NOLIN1 с 1 по N-й узел
            u = 1
            while u < new_topic.N + 1:
                u += 1
                u = int(u)
                file.write(
                    "NOLIN1  1       {: <8.1f}2       1.00    {: <8.1f}1       {: <8.1f}\n".format(u, u, u + 100))
            file.write("\n\n")

            #Запись TABLED1 (ветровые усилия)
            #если ракета с наземным стартом
            d = d0 = new_topic.d0
            if (new_topic.start_rocket == 1):
                po_vozduh = float(1225)
                po_vozduh = Decimal(po_vozduh)
                P_veter = ((po_vozduh * new_topic.V_sredy * new_topic.V_sredy) / 2) * (Decimal('0.1') * new_topic.d0)
                u = 1
                while u < new_topic.N + 1:
                    u += 1
                    u = int(u)
                    vychitanie = (new_topic.L + 1) - ((u * k) - k)
                    slozhenie = (new_topic.L + 1) - ((u * k) - k) + k
                    file.write("TABLED1 {: <8d}\n        0.00    0.00    {: <8.1f}0.00    {: <8.1f}{: <8.1f}100.0   {: <8.1f}\n        ENDT\n".format(u + 100, vychitanie, slozhenie, P_veter, P_veter))
                file.write("\n")
            else:
                po_vody = float(997)
                po_vody = Decimal(po_vody)
                P_vody = ((po_vody * new_topic.V_sredy * new_topic.V_sredy) / 2) * (Decimal('0.1') * new_topic.d0)
                u = 1
                while u < new_topic.N + 1:
                    u += 1
                    u = int(u)
                    vychitanie = (new_topic.L + 1) - ((u * k) - k)
                    slozhenie = (new_topic.L + 1) - ((u * k) - k) + k
                    file.write("TABLED1 {: <8d}\n        0.00    0.00    {: <8.1f}0.00    {: <8.1f}{: <8.1f}100.0   {: <8.1f}\n        ENDT\n".format(u + 100, vychitanie, slozhenie, P_vody, P_vody))
                file.write("\n")

            # Запись SPC с 1 по N-й узел
            u = 1
            while u < new_topic.N + 1:
                u += 1
                u = int(u)
                file.write("SPC     10      {: <8d}345\n".format(u))
            file.write("\n\n")

            # Запись SPC с 100001 по 10000N-й узел контейнера
            u = 1
            while u < new_topic.N + 11:
                u += 1
                u = int(u)
                file.write("SPC     10      {: <8d}345\n".format(u + 100000))
            file.write("\n\n")

            # Запись SPC окислитель
            u = o1
            while u < o + 1:
                u += 1
                u = int(u)
                file.write("SPC     10      {: <8d}345\n".format(u))
            file.write("\n\n")

            # Запись SPC горючее
            u = g1
            while u < g + 1:
                u += 1
                u = int(u)
                file.write("SPC     10      {: <8d}345\n".format(u))
            file.write("\n\n")



            if (new_topic.kolichestvo_amort == 2):
                # Запись GRID узлы скольжения

                a1 = (new_topic.X1 / k)  # узел первого амортизатора
                a2 = (new_topic.X2 / k)  # узел второго амортизатора


                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200001, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200001, new_topic.X2, coy))
                file.write("\n\n")

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200011, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200011, new_topic.X2, coy))
                file.write("\n\n")

                coy_kont = coy * 2

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 300011, new_topic.X1, coy_kont))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 300011, new_topic.X2, coy_kont))
                file.write("\n\n")

                # Запись CELAS1 узлов скольжения

                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200001, a1 + 1, a1 + 200001))
                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200001, a2 + 1, a2 + 200001))
                file.write("\n\n")

                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200011, a1 + 200011, a1 + 300011))
                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200011, a2 + 200011, a2 + 300011))
                file.write("\n\n")

                # Запись PELAS узлов скольжения (жесткость?)

                file.write("PELAS   2       {: <8.1f}+7\n\n".format(new_topic.zhestkost_amort))

                # Запись RBE2 узлов скольжения

                i1 = 1

                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a1 + 400001, a1 + 1, i1, a1 + 200001, a1 + 200011, a1 + 300011))
                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a2 + 400001, a2 + 1, i1, a2 + 200001, a2 + 200011, a2 + 300011))
                file.write("\n\n")

                i2 = 2

                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a1 + 400011, a1 + 1, i2, a1 + 300011))
                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a2 + 400011, a2 + 1, i2, a2 + 300011))
                file.write("\n\n")

                # Запись BLSEG

                file.write("BLSEG   1       {: <8.1f}{: <8.1f}\n".format(a1 + 1, a1 + 200001))
                file.write("BLSEG   3       {: <8.1f}{: <8.1f}\n".format(a2 + 1, a2 + 200001))
                file.write("\n")

                file.write("BLSEG   7       {: <8.1f}{: <8.1f}\n".format(a1 + 300011, a1 + 200011))
                file.write("BLSEG   8       {: <8.1f}{: <8.1f}\n".format(a2 + 300011, a2 + 200011))
                file.write("\n\n")

                # Запись BCONP

                file.write("BCONP   1       1       2               1.0     10      1       1\n")
                file.write("BCONP   2       3       2               1.0     10      1       1\n")
                file.write("\n")

                file.write("BCONP   6       7       2               1.0     10      1       3\n")
                file.write("BCONP   7       8       2               1.0     10      1       3\n")

                # Запись SPC опорных узлов контейнера

                file.write("\n\n")
                file.write("SPC     10      {: <8.1f}23456\n".format(a1 + 100001))
                file.write("SPC     10      {: <8.1f}23456\n".format(a2 + 100001))



            elif (new_topic.kolichestvo_amort == 3):

                # Запись GRID узлы скольжения

                a1 = (new_topic.X1 / k)  # узел первого амортизатора
                a2 = (new_topic.X2 / k)  # узел второго амортизатора

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200001, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200001, new_topic.X2, coy))
                file.write("\n\n")

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200011, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200011, new_topic.X2, coy))
                file.write("\n\n")

                coy_kont = coy * 2

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 300011, new_topic.X1, coy_kont))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 300011, new_topic.X2, coy_kont))
                file.write("\n\n")

                # Запись CELAS1 узлов скольжения

                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200001, a1 + 1, a1 + 200001))
                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200001, a2 + 1, a2 + 200001))
                file.write("\n\n")

                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200011, a1 + 200011, a1 + 300011))
                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200011, a2 + 200011, a2 + 300011))
                file.write("\n\n")

                # Запись PELAS узлов скольжения (жесткость?)

                file.write("PELAS   2       {: <8.1f}+7\n\n".format(new_topic.zhestkost_amort))

                # Запись RBE2 узлов скольжения

                i1 = 1

                file.write(
                    "RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a1 + 400001, a1 + 1, i1,
                                                                                             a1 + 200001, a1 + 200011,
                                                                                             a1 + 300011))
                file.write(
                    "RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a2 + 400001, a2 + 1, i1,
                                                                                             a2 + 200001, a2 + 200011,
                                                                                             a2 + 300011))
                file.write("\n\n")

                i2 = 2

                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a1 + 400011, a1 + 1, i2, a1 + 300011))
                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a2 + 400011, a2 + 1, i2, a2 + 300011))
                file.write("\n\n")

                # Запись BLSEG

                file.write("BLSEG   1       {: <8.1f}{: <8.1f}\n".format(a1 + 1, a1 + 200001))
                file.write("BLSEG   3       {: <8.1f}{: <8.1f}\n".format(a2 + 1, a2 + 200001))
                file.write("\n")

                file.write("BLSEG   7       {: <8.1f}{: <8.1f}\n".format(a1 + 300011, a1 + 200011))
                file.write("BLSEG   8       {: <8.1f}{: <8.1f}\n".format(a2 + 300011, a2 + 200011))
                file.write("\n\n")

                # Запись BCONP

                file.write("BCONP   1       1       2               1.0     10      1       1\n")
                file.write("BCONP   2       3       2               1.0     10      1       1\n")
                file.write("\n")

                file.write("BCONP   6       7       2               1.0     10      1       3\n")
                file.write("BCONP   7       8       2               1.0     10      1       3\n")

                # Запись SPC опорных узлов контейнера

                file.write("\n\n")
                file.write("SPC     10      {: <8.1f}23456\n".format(a1 + 100001))
                file.write("SPC     10      {: <8.1f}23456\n".format(a2 + 100001))

            elif (new_topic.kolichestvo_amort == 4):

                # Запись GRID узлы скольжения

                a1 = (new_topic.X1 / k)  # узел первого амортизатора
                a2 = (new_topic.X2 / k)  # узел второго амортизатора

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200001, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200001, new_topic.X2, coy))
                file.write("\n\n")

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200011, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200011, new_topic.X2, coy))
                file.write("\n\n")

                coy_kont = coy * 2

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 300011, new_topic.X1, coy_kont))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 300011, new_topic.X2, coy_kont))
                file.write("\n\n")

                # Запись CELAS1 узлов скольжения

                file.write(
                    "CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200001, a1 + 1, a1 + 200001))
                file.write(
                    "CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200001, a2 + 1, a2 + 200001))
                file.write("\n\n")

                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200011, a1 + 200011,
                                                                                           a1 + 300011))
                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200011, a2 + 200011,
                                                                                           a2 + 300011))
                file.write("\n\n")

                # Запись PELAS узлов скольжения (жесткость?)

                file.write("PELAS   2       {: <8.1f}+7\n\n".format(new_topic.zhestkost_amort))

                # Запись RBE2 узлов скольжения

                i1 = 1

                file.write(
                    "RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a1 + 400001, a1 + 1, i1,
                                                                                             a1 + 200001, a1 + 200011,
                                                                                             a1 + 300011))
                file.write(
                    "RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a2 + 400001, a2 + 1, i1,
                                                                                             a2 + 200001, a2 + 200011,
                                                                                             a2 + 300011))
                file.write("\n\n")

                i2 = 2

                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a1 + 400011, a1 + 1, i2, a1 + 300011))
                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a2 + 400011, a2 + 1, i2, a2 + 300011))
                file.write("\n\n")

                # Запись BLSEG

                file.write("BLSEG   1       {: <8.1f}{: <8.1f}\n".format(a1 + 1, a1 + 200001))
                file.write("BLSEG   3       {: <8.1f}{: <8.1f}\n".format(a2 + 1, a2 + 200001))
                file.write("\n")

                file.write("BLSEG   7       {: <8.1f}{: <8.1f}\n".format(a1 + 300011, a1 + 200011))
                file.write("BLSEG   8       {: <8.1f}{: <8.1f}\n".format(a2 + 300011, a2 + 200011))
                file.write("\n\n")

                # Запись BCONP

                file.write("BCONP   1       1       2               1.0     10      1       1\n")
                file.write("BCONP   2       3       2               1.0     10      1       1\n")
                file.write("\n")

                file.write("BCONP   6       7       2               1.0     10      1       3\n")
                file.write("BCONP   7       8       2               1.0     10      1       3\n")

                # Запись SPC опорных узлов контейнера

                file.write("\n\n")
                file.write("SPC     10      {: <8.1f}23456\n".format(a1 + 100001))
                file.write("SPC     10      {: <8.1f}23456\n".format(a2 + 100001))

            else:

                # Запись GRID узлы скольжения

                a1 = (new_topic.X1 / k)  # узел первого амортизатора
                a2 = (new_topic.X2 / k)  # узел второго амортизатора

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200001, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200001, new_topic.X2, coy))
                file.write("\n\n")

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 200011, new_topic.X1, coy))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 200011, new_topic.X2, coy))
                file.write("\n\n")

                coy_kont = coy * 2

                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a1 + 300011, new_topic.X1, coy_kont))
                file.write("GRID    {: <8.1f}        {: <8f}{: <8.1f}0.00\n".format(a2 + 300011, new_topic.X2, coy_kont))
                file.write("\n\n")

                # Запись CELAS1 узлов скольжения

                file.write(
                    "CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200001, a1 + 1, a1 + 200001))
                file.write(
                    "CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200001, a2 + 1, a2 + 200001))
                file.write("\n\n")

                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a1 + 200011, a1 + 200011,
                                                                                           a1 + 300011))
                file.write("CELAS1  {: <8.1f}2       {: <8.1f}2       {: <8.1f}2\n".format(a2 + 200011, a2 + 200011,
                                                                                           a2 + 300011))
                file.write("\n\n")

                # Запись PELAS узлов скольжения (жесткость?)

                file.write("PELAS   2       {: <8.1f}+7\n\n".format(new_topic.zhestkost_amort))

                # Запись RBE2 узлов скольжения

                i1 = 1

                file.write(
                    "RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a1 + 400001, a1 + 1, i1,
                                                                                             a1 + 200001, a1 + 200011,
                                                                                             a1 + 300011))
                file.write(
                    "RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}{: <8.1f}{: <8.1f}\n".format(a2 + 400001, a2 + 1, i1,
                                                                                             a2 + 200001, a2 + 200011,
                                                                                             a2 + 300011))
                file.write("\n\n")

                i2 = 2

                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a1 + 400011, a1 + 1, i2, a1 + 300011))
                file.write("RBE2    {: <8.1f}{: <8.1f} {: <8d}{: <8.1f}\n".format(a2 + 400011, a2 + 1, i2, a2 + 300011))
                file.write("\n\n")

                # Запись BLSEG

                file.write("BLSEG   1       {: <8.1f}{: <8.1f}\n".format(a1 + 1, a1 + 200001))
                file.write("BLSEG   3       {: <8.1f}{: <8.1f}\n".format(a2 + 1, a2 + 200001))
                file.write("\n")

                file.write("BLSEG   7       {: <8.1f}{: <8.1f}\n".format(a1 + 300011, a1 + 200011))
                file.write("BLSEG   8       {: <8.1f}{: <8.1f}\n".format(a2 + 300011, a2 + 200011))
                file.write("\n\n")

                # Запись BCONP

                file.write("BCONP   1       1       2               1.0     10      1       1\n")
                file.write("BCONP   2       3       2               1.0     10      1       1\n")
                file.write("\n")

                file.write("BCONP   6       7       2               1.0     10      1       3\n")
                file.write("BCONP   7       8       2               1.0     10      1       3\n")

                # Запись SPC опорных узлов контейнера

                file.write("\n\n")
                file.write("SPC     10      {: <8.1f}23456\n".format(a1 + 100001))
                file.write("SPC     10      {: <8.1f}23456\n".format(a2 + 100001))

            file.write("\n\n")

            # Запись BLSEG

            file.write("BLSEG   2       100001  THRU    {: <8.1f}".format(new_topic.N + 100010))
            file.write("\n\n")

            # Запись BFRIC

            file.write("BFRIC   10                      0.1")
            file.write("\n\n")

            # Запись CORD2R

            file.write(
                "CORD2R  1               0.0     1.1     0.0     0.0     1.1     -1.0\n        1.0     1.1     0.0")
            file.write("\n\n")

            # Запись CORD2R

            file.write(
                "CORD2R  3               0.0     -1.1    0.0     0.0     -1.1    1.0\n        1.0     -1.1    0.0")
            file.write("\n\n")

            # Запись TABLED1 (тяга)
            if (new_topic.P12 < 10000000 and new_topic.P12 > 1000000 or new_topic.P12 == 1000000):

                file.write("TABLED1 411\n        0.0     0.0     1.0     0.0     {: <8.3f}{: <8.5f}{: <8.3f}{: <8.5f}\n".format(new_topic.t_p1, new_topic.P1, new_topic.t_p2, new_topic.P2))
                file.write("        {: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}\n".format(new_topic.t_p3, new_topic.P3, new_topic.t_p4, new_topic.P4, new_topic.t_p5, new_topic.P5, new_topic.t_p6, new_topic.P6))
                file.write("        {: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}\n".format(new_topic.t_p7, new_topic.P7, new_topic.t_p8, new_topic.P8, new_topic.t_p9, new_topic.P9, new_topic.t_p10, new_topic.P10))
                file.write("        {: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}ENDT\n".format(new_topic.t_p11, new_topic.P11, new_topic.t_p12, new_topic.P12, new_topic.t_p13, new_topic.P13))

            elif (new_topic.P12 > 100000 or new_topic.P12 == 100000 and new_topic.P12 < 1000000):

                file.write("TABLED1 411\n        0.0     0.0     1.0     0.0     {: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}\n".format(new_topic.t_p1, new_topic.P1, new_topic.t_p2, new_topic.P2))
                file.write("        {: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}\n".format(new_topic.t_p3, new_topic.P3, new_topic.t_p4, new_topic.P4, new_topic.t_p5, new_topic.P5, new_topic.t_p6, new_topic.P6))
                file.write("        {: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}\n".format(new_topic.t_p7, new_topic.P7, new_topic.t_p8, new_topic.P8, new_topic.t_p9, new_topic.P9, new_topic.t_p10, new_topic.P10))
                file.write("        {: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}{: <8.3f}{: <8.0f}ENDT\n".format(new_topic.t_p11, new_topic.P11, new_topic.t_p12, new_topic.P12, new_topic.t_p13, new_topic.P13))

            elif (new_topic.P12 < 100000 and new_topic.P12 > 10000 or new_topic.P12 == 10000):

                file.write("TABLED1 411\n        0.0     0.0     1.0     0.0     {: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}\n".format(new_topic.t_p1, new_topic.P1, new_topic.t_p2, new_topic.P2))
                file.write("        {: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}\n".format(new_topic.t_p3, new_topic.P3, new_topic.t_p4, new_topic.P4, new_topic.t_p5, new_topic.P5, new_topic.t_p6, new_topic.P6))
                file.write("        {: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}\n".format(new_topic.t_p7, new_topic.P7, new_topic.t_p8, new_topic.P8, new_topic.t_p9, new_topic.P9, new_topic.t_p10, new_topic.P10))
                file.write("        {: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}{: <8.3f}{: <8.1f}ENDT\n".format(new_topic.t_p11, new_topic.P11, new_topic.t_p12, new_topic.P12, new_topic.t_p13, new_topic.P13))

            elif (new_topic.P12 > 1000 and new_topic.P12 < 10000 or new_topic.P12 == 1000):

                file.write("TABLED1 411\n        0.0     0.0     1.0     0.0     {: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}\n".format(new_topic.t_p1, new_topic.P1, new_topic.t_p2, new_topic.P2))
                file.write("        {: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}\n".format(new_topic.t_p3, new_topic.P3, new_topic.t_p4, new_topic.P4, new_topic.t_p5, new_topic.P5, new_topic.t_p6, new_topic.P6))
                file.write("        {: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}\n".format(new_topic.t_p7, new_topic.P7, new_topic.t_p8, new_topic.P8, new_topic.t_p9, new_topic.P9, new_topic.t_p10, new_topic.P10))
                file.write("        {: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}{: <8.3f}{: <8.2f}ENDT\n".format(new_topic.t_p11, new_topic.P11, new_topic.t_p12, new_topic.P12, new_topic.t_p13, new_topic.P13))

            elif (new_topic.P12 > 10000000 and new_topic.P12 < 100000000 or new_topic.P12 == 10000000):

                file.write("TABLED1 411\n        0.0     0.0     1.0     0.0     {: <8.3f}{: <8.5f}{: <8.3f}{: <8.5f}\n".format(new_topic.t_p1, new_topic.P1 / 1000, new_topic.t_p2, new_topic.P2 / 1000))
                file.write("        {: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}\n".format(new_topic.t_p3, new_topic.P3 / 1000, new_topic.t_p4, new_topic.P4 / 1000, new_topic.t_p5, new_topic.P5 / 1000, new_topic.t_p6, new_topic.P6 / 1000))
                file.write("        {: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}\n".format(new_topic.t_p7, new_topic.P7 / 1000, new_topic.t_p8, new_topic.P8 / 1000, new_topic.t_p9, new_topic.P9 / 1000, new_topic.t_p10, new_topic.P10 / 1000))
                file.write("        {: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}{: <8.3f}{: <8.4f}ENDT\n".format(new_topic.t_p11, new_topic.P11 / 1000, new_topic.t_p12, new_topic.P12 / 1000, new_topic.t_p13, new_topic.P13 / 1000))

            else:

                file.write("TABLED1 411\n        0.0     0.0     1.0     0.0     {: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}\n".format(new_topic.t_p1, new_topic.P1, new_topic.t_p2, new_topic.P2))
                file.write("        {: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}\n".format(new_topic.t_p3, new_topic.P3, new_topic.t_p4, new_topic.P4, new_topic.t_p5, new_topic.P5, new_topic.t_p6, new_topic.P6))
                file.write("        {: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}\n".format(new_topic.t_p7, new_topic.P7, new_topic.t_p8, new_topic.P8, new_topic.t_p9, new_topic.P9, new_topic.t_p10, new_topic.P10))
                file.write("        {: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}{: <8.3f}{: <7.4f}ENDT\n".format(new_topic.t_p11, new_topic.P11, new_topic.t_p12, new_topic.P12, new_topic.t_p13, new_topic.P13))

            file.write("\n\n")

            # Запись TLOAD1

            file.write("TLOAD1  210     110     0       0       411")
            file.write("\n\n")

            # Запись FORCE

            file.write("FORCE   111     1       0       1.0     1.0     0.0")
            file.write("\n\n")

            # Запись LSEQ

            file.write("LSEQ    100     110     111")
            file.write("\n\n")

            # Запись DLOAD

            file.write("DLOAD   333     1.00    1.00    210     1.00    310")
            file.write("\n\n")

            # Запись LOAD

            file.write("LOAD    444     1.0     1.0     222")
            file.write("\n\n")

            # Запись MAT1

            massa_korpusa = new_topic.m - new_topic.m_gch - new_topic.m_cy - new_topic.m_dy - new_topic.mo - new_topic.mg
            plotnost1 = massa_korpusa / (((Decimal('3.14') * new_topic.d0 * new_topic.d0 / Decimal('4')) - (Decimal('3.14') * (new_topic.d0 - Decimal('0.003')) * (new_topic.d0 - Decimal('0.003')) / Decimal('4'))) * new_topic.L)

            file.write("MAT1    1       {: <2.1f}+10          {: <8.2f}{: <8.1f}\n".format(new_topic.modul_unga1, new_topic.koeff_puass1, plotnost1))
            file.write("MAT1    2       {: <2.1f}+10          {: <8.2f}{: <8.3f}".format(new_topic.modul_unga2, new_topic.koeff_puass2, new_topic.plotnost2))
            file.write("\n\n")

            # Запись PBARL

            file.write("PBARL   1       1               TUBE2\n        {: <8.2f}0.003".format(new_topic.d0))
            file.write("\n")
            file.write("PBARL   2       2               TUBE2\n        {: <8.2f}0.0175".format(new_topic.d0 + Decimal('0.2')))
            file.write("\n\n")

            # Запись LSEQ для ускорения свободного падения

            file.write("LSEQ    100     210     222")
            file.write("\n")

            # Запись GRAV для ускорения свободного падения

            file.write("GRAV    222             -9.81   1.0     0.0     0.0")
            file.write("\n")

            # Запись TLOAD1 для ускорения свободного падения

            file.write("TLOAD1  310     210     0       0       511")
            file.write("\n")

            # Запись TABLED1 для ускорения свободного падения

            file.write("TABLED1 511\n        0.0     1.0     30.0    1.0     ENDT")
            file.write("\n\n")

            # Запись GRID для продольной амортизации контейнера

            file.write("GRID    9000            0.0     {: <8.3f}0.0".format((new_topic.d0 / 2) + Decimal('0.1')))
            file.write("\n\n")

            # Запись PELAS

            file.write("PELAS   9000    658.6+6")
            file.write("\n\n")

            # Запись CELAS1

            file.write("CELAS1  9000    9000    100001  1       9000    1")
            file.write("\n\n")

            # Запись SPC для опорного стола

            file.write("SPC     10      9000    123456\n")
            file.write("\n\n")

            # Запись TSTEPNL

            n_time = 0.001  # шаг по времени
            n_time = Decimal(n_time)
            t_shoda = (new_topic.t / n_time)  # время схода поясов амортизации

            file.write("TSTEPNL 1       10      0.1     1       ADAPT\n")
            file.write("TSTEPNL 2       {: <8.0f}{: <8.3f}1       ADAPT\n".format(t_shoda, n_time))
            file.write("\n\n")

            file.write("ENDDATA")





































            file.close()
            return redirect('bdf:rockets_bdf_all')

    context = {'form': form}
    return render(request, 'bdf/rocket_bdf_new.html', context)


@login_required()
def rocket_bdf_edit(request, rocket_id):
    #редактируем существующий проект
    bdf_edit = Rockets_bdf.objects.get(id=rocket_id)
    if bdf_edit.owner != request.user:
        raise Http404

    if request.method != 'POST':
        #Исходный запрос, форма заполняется данными текущей записи
        form = Rockets_bdfForm(instance=bdf_edit)

    else:
        #Отправка данных POST
        form = Rockets_bdfForm(instance=bdf_edit, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('bdf:rocket', rocket_id=bdf_edit.id)

    context = {'bdf_edit' : bdf_edit, 'form': form}
    return render(request, 'bdf/rocket_bdf_edit.html', context)

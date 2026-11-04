"""Update only marked, data-generated blocks in the editable manuscript.
No scientific prose is regenerated. No PDF is compiled. Plots are inline PGFPlots.
Usage: python code/make_assets.py --manuscript /path/to/coboson_paper_draft.tex
"""
from pathlib import Path
import argparse,json,re,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'data'
read=lambda n:json.loads((DATA/n).read_text())

def table(header,rows,align=None):
    return '\\begin{tabular}{'+(align or 'l'+'r'*(len(header)-1))+'}\n\\toprule\n'+' & '.join(header)+r'\\'+'\n\\midrule\n'+'\n'.join(' & '.join(map(str,row))+r'\\' for row in rows)+'\n\\bottomrule\n\\end{tabular}'

def coords(xy):return ' '.join('(%s,%s)'%(format(x,'.9g'),format(y,'.9g')) for x,y in xy if np.isfinite(y))
def plot(xy,style,legend=None):return '\\addplot['+style+'] coordinates {'+coords(xy)+'};\n'+('\\addlegendentry{'+legend+'}\n' if legend else '')

def harmonic(S,m,n):
    a=(2*m+1)/math.sqrt(S);b=(2*n+1)*math.pi/(2*math.sqrt(S));v=[]
    for order in [0,1]:
        for sign in [-1,1]:
            U=np.array([[math.cos(a),-sign*math.sin(a)],[sign*math.sin(a),math.cos(a)]],complex)
            for t in [-1,1]:
                V=np.array([[math.cos(b),-1j*t*math.sin(b)],[-1j*t*math.sin(b),math.cos(b)]])
                v.append(((U@V) if order==0 else (V@U))[:,0])
    return float(np.sqrt(max(0.,sum(np.vdot(u,w)**S for u in v for w in v).real/16)))


def generate():
    flat=read('legacy_flat_scan.json');nf=read('legacy_nonflat_scan.json');fresh=read('fresh_flat_checks.json');blocks={}
    bell=read('bell_raw_scan.json')+read('bell_raw_8000.json')
    def bellval(S,tie):
        return next((b['bell_raw'] for b in bell if b['S']==S and b['tie']==tie),None)
    selected=[8,12,16,24,32,64,128,256,512,1024,2050,3956,8000];rows=[]
    for S in selected:
        for d in [a for a in flat if a['S']==S]:
            new=next((a for a in fresh if a['S']==S and a['tie']==d['tie']),d)
            # Keep original schema plus independently refreshed values when present.
            a=d|new;p=a.get('p');t=a.get('t');bl=a.get('bloch');B=bellval(S,a['tie'])
            rows.append([str(S),'$+$' if a['tie']>0 else '$-$',f"{a['dD']:.4f}",f"{a['eps']:.4f}",f'{t:.4f}' if t is not None else '--',f'{bl:.4f}' if bl is not None else '--',f'{max(0,p):.6f}' if p is not None else '--',f"{a['praw']:.4f}",f'{B:.3f}' if B is not None else '--',str(a['naz']) if a['naz'] else '--'])
    rows.append(['$\\infty$','--','0','0','1','0.8522','0.068350','0.0683','2.828','--'])
    blocks['flat_table']=table(['$S$','tie','$\\delta_D$','$\\varepsilon_0$','$t$','$|\\vec m|/t$','$p_{\\rm corr}$','$p_{\\rm raw}$','$\\mathcal B_{\\rm raw}$','edges'],rows)
    bp=[b for b in bell if b['tie']>0 and b['S']<=4096];bm=[b for b in bell if b['tie']<0 and b['S']<=4096]
    g='\\begin{tikzpicture}\n\\begin{axis}[width=0.62\\textwidth,height=5.2cm,xmode=log,xlabel={$S$},ylabel={Bell value of the raw state},ymin=2,ymax=2.9,grid=major,tick label style={font=\\scriptsize},label style={font=\\small},legend style={font=\\scriptsize,at={(0.5,-0.28)},anchor=north,draw=none,legend columns=2},legend cell align=left]\n'
    g+=plot([(b['S'],b['bell_raw']) for b in bp],'green!50!black,only marks,mark=*,mark size=.6pt','raw sequential state, tie $+$')
    g+=plot([(b['S'],b['bell_raw']) for b in bm],'orange!80!black,only marks,mark=triangle,mark size=1.6pt','tie $-$')
    g+=plot([(4,2*np.sqrt(2)),(4096,2*np.sqrt(2))],'black,dotted,no marks','$2\\sqrt2$ (exact singlet)')
    g+=plot([(4,2),(4096,2)],'gray,dashed,no marks','local bound $2$')
    blocks['bell_figure']=g+'\\end{axis}\n\\end{tikzpicture}'
    blocks['robustness_table']=table(['$S$','$r$','$p$','$t$'],[[d['S'],r'$1-10^{-8}$' if d['r']<1 else (r'$1+10^{-8}$' if d['r']>1 else '$1$'),f"{d['p']:.8f}",f"{d['t']:.6f}"] for d in read('scale_sensitivity.json') if d['S'] in [8,16]])
    dense=read('fresh_dense_nonflat.json');rows=[]
    for d in dense:
        tag=('geometric $z=' if d['family']=='geometric' else 'algebraic $w=')+f"{d['parameter']:g}$"
        rows.append([tag,d['S'],f"{d['P']:.4f}",f"{d['dD']:.3f}",f"{d['eps']:.3f}",f"{d['results']['0.4']['p']:.6f}",f"{d['results']['0.6']['p']:.6f}"])
    blocks['dense_nonflat_table']=table(['model','$S$','$P$','$\\delta_D$','$\\varepsilon_0$','$p_{0.4}$','$p_{0.6}$'],rows)
    last=[a for a in nf if a['S']==19];rows=[]
    for d in last:rows.append([f"{d['z']:.1f}",f"{1/d['P']:.2f}",f"{d['z']**19:.4f}",f"{d['dD']:.3f}",f"{d['eps']:.3f}",f"{d['t_0.4']:.3f}",f"{d['p_0.4']:.4f}",f"{d['t_0.6']:.3f}",f"{d['p_0.6']:.4f}"])
    blocks['nonflat_estimate_table']=table(['$z$','$\\mathcal K_S$','$z^S$','$\\delta_D$','$\\varepsilon_0$','$t_{0.4}$','$p_{0.4}$','$t_{0.6}$','$p_{0.6}$'],rows)
    rows=[]
    for d in read('lanczos_sensitivity.json'):
        rows.append([d['requested_steps']]+[f"{d['results'][k][key]:.6f}" for k in ['0.4','0.6'] for key in ['t','p']])
    blocks['lanczos_table']=table(['steps','$t_{0.4}$','$p_{0.4}$','$t_{0.6}$','$p_{0.6}$'],rows)
    harm=[];rows=[]
    for m,n in [(0,0),(3,0),(8,0),(0,8),(3,3)]:
        a,b=harmonic(256,m,n),harmonic(4096,m,n);rows.append([m,n,f'{a:.6f}',f'{b:.6f}']);harm.extend([dict(S=256,m=m,n=n,defect=a),dict(S=4096,m=m,n=n,defect=b)])
    blocks['harmonics_table']=table(['$m$','$n$','$S=256$','$S=4096$'],rows)
    # Two panels; each legend sits outside the axes to avoid covering data.
    sty=r'width=0.46\textwidth,height=5.1cm,grid=major,tick label style={font=\scriptsize},label style={font=\small},legend style={font=\scriptsize,at={(0.5,-0.24)},anchor=north,draw=none},legend cell align=left'
    p=[a for a in flat if a['tie']>0];m=[a for a in flat if a['tie']<0]
    g='\\begin{tikzpicture}\n\\begin{groupplot}[group style={group size=2 by 1,horizontal sep=1.5cm},'+sty+']\n'
    g+=r'\nextgroupplot[xmode=log,ymode=log,xlabel={$S$},ylabel={vacuum defect},ymin=0.0009,ymax=2.5]'+'\n'
    g+=plot([(a['S'],a['dD']) for a in p],'blue,no marks','displacement')
    g+=plot([(a['S'],a['eps']) for a in p],'red,only marks,mark=*,mark size=0.5pt','hard bin, tie $+$')
    g+=plot([(a['S'],a['eps']) for a in m],'orange!80!black,only marks,mark=triangle,mark size=1.6pt','hard bin, tie $-$')
    L=1+np.pi**2/4;c=np.pi*np.sqrt(L+4*L*L/9)
    g+=plot([(S,c/S) for S in [8,32,128,512,2048,8000]],'blue,dashed,no marks','$1/S$ leading term')
    g+=r'\nextgroupplot[xmode=log,xlabel={$S$},ylabel={probability (\%)},ymin=0,ymax=16]'+'\n'
    g+=plot([(a['S'],100*a['praw']) for a in p if 'p' in a],'green!50!black,only marks,mark=*,mark size=.5pt','raw sequential (not a singlet)')
    g+=plot([(a['S'],100*max(0,a['p'])) for a in p if 'p' in a],'red,only marks,mark=*,mark size=.6pt','corrected: exact singlet')
    g+=plot([(4,6.83497058887),(4096,6.83497058887)],'black,dotted,no marks','oscillator value')
    blocks['rank_figure']=g+'\\end{groupplot}\n\\end{tikzpicture}'
    colors=['blue','green!50!black','violet','red','orange!80!black'];zs=sorted(set(d['z'] for d in nf))
    g='\\begin{tikzpicture}\n\\begin{groupplot}[group style={group size=2 by 1,horizontal sep=1.5cm},'+sty+',legend columns=2]\n'
    g+=r'\nextgroupplot[xlabel={retained modes $S$},ylabel={$p_{0.6}$ (\%)},ymin=0,ymax=4.2]'+'\n'
    for z,col in zip(zs,colors):g+=plot([(d['S'],100*d['p_0.6']) for d in nf if d['z']==z and d['S']>=6],col+',mark=*,mark size=1pt','$z='+str(z)+'$')
    g+=r'\nextgroupplot[xlabel={purity $P$ at $S=19$},ymin=0,ymax=1.5,legend columns=3]'+'\n'
    last=sorted([d for d in nf if d['S']==19],key=lambda d:d['P'])
    g+=plot([(d['P'],d['dD']) for d in last],'blue,mark=square*,mark size=1.3pt','$\\delta_D$')
    g+=plot([(d['P'],d['eps']) for d in last],'red,mark=*,mark size=1.3pt','$\\varepsilon_{\\rm vac}$')
    g+=plot([(d['P'],d['t_0.6']) for d in last],'green!50!black,mark=diamond*,mark size=1.5pt','$t_{0.6}$')
    g+=plot([(d['P'],d['w_at_1']) for d in last],'black,mark=x,mark size=2pt','weight at $K=\\pm1$')
    g+=plot([(d['P'],10*d['p_0.6']) for d in last],'violet,mark=triangle*,mark size=1.5pt','$10\\,p_{0.6}$')
    g+=plot([(d['P'],d['praw']) for d in last],'orange!80!black,mark=triangle,mark size=1.5pt,mark options={rotate=180}','$p_{\\rm raw}$')
    blocks['nonflat_figure']=g+'\\end{groupplot}\n\\end{tikzpicture}'
    # Aligned panels separate model probabilities from the universal bound.
    g=r'''\definecolor{cutblue}{RGB}{0,114,178}
\definecolor{cutorange}{RGB}{230,159,0}
\definecolor{cutgreen}{RGB}{0,158,115}
\definecolor{cutred}{RGB}{213,94,0}
\definecolor{cutpurple}{RGB}{160,88,153}
\begin{tikzpicture}
\begin{groupplot}[group style={group size=1 by 2,vertical sep=1.25cm},width=.87\textwidth,xmin=0,xmax=1,xtick={0,0.2,0.4,0.6,0.8,1},grid=major,grid style={gray!18},tick label style={font=\small},label style={font=\small}]
\nextgroupplot[height=5.1cm,ymin=0,ymax=5,ytick={0,1,2,3,4,5},xticklabels=\empty,ylabel={singlet probability (\%)},title={(a) Preparation probability},title style={font=\small,at={(0,1.03)},anchor=south west},legend to name=cutofflegend,legend columns=5,legend style={font=\scriptsize,draw=none,column sep=6pt},legend cell align=left]
\draw[gray!65,dashed] (axis cs:0.4,0)--(axis cs:0.4,5);
\draw[gray!65,dashed] (axis cs:0.6,0)--(axis cs:0.6,5);
'''
    cs=read('cutoff_curves.json')
    curves=[('flat_8','cutblue,solid','flat $S=8$'),
            ('flat_64','cutorange,densely dashed','flat $S=64$'),
            ('geometric_0.5','cutgreen,dash dot','geometric $z=0.5$'),
            ('geometric_0.7','cutred,dashed','geometric $z=0.7$'),
            ('algebraic_6.0','cutpurple,densely dotted','algebraic $w=6$')]
    for key,style,label in curves:
        g+=plot([(d['kappa'],max(0,100*d['p'])) for d in cs[key]],style+',thick,const plot,no marks',label)
    g+=r'''\nextgroupplot[height=3.8cm,ymin=0,ymax=1.5,ytick={0,0.5,1,1.41421356237},yticklabels={$0$,$0.5$,$1$,$\sqrt2$},xlabel={filter cutoff $\kappa$},ylabel={bound $C(\kappa)$},title={(b) Allowed measurement correction},title style={font=\small,at={(0,1.03)},anchor=south west}]
\draw[gray!65,dashed] (axis cs:0.4,0)--(axis cs:0.4,1.5);
\draw[gray!65,dashed] (axis cs:0.6,0)--(axis cs:0.6,1.5);
'''
    # Parameterise kappa=sin(theta) to resolve the endpoint without a kink.
    g+=plot([(np.sin(t),2*np.sin(t/2)) for t in np.linspace(0,np.pi/2,201)],'black,thick,no marks')
    for k in [.4,.6]:
        c=np.sqrt(2*(1-np.sqrt(1-k*k)))
        g+=plot([(k,c)],'black,only marks,mark=*,mark size=1.8pt')
        g+=f'\\node[font=\\scriptsize,anchor=south east,fill=white,inner sep=1.5pt] at (axis cs:{k},{c}) {{$C\\simeq{c:.3f}$}};\n'
    g+=r'\addplot[black,only marks,mark=o,mark options={fill=white},mark size=2pt] coordinates {(1,1.41421356237)};'+'\n'
    blocks['cutoff_figure']=g+'\\end{groupplot}\n\\end{tikzpicture}\n\\par\\smallskip\\pgfplotslegendfromname{cutofflegend}'
    return blocks


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manuscript',type=Path,required=True);a=p.parse_args();s=a.manuscript.read_text()
    for name,value in generate().items():
        pat=r'(% BEGIN GENERATED '+name+r'\n).*?(\n?% END GENERATED '+name+r')'
        s,n=re.subn(pat,lambda m:m.group(1)+value+'\n'+m.group(2).lstrip('\n'),s,flags=re.S)
        if n!=1:raise ValueError('Expected one marked block: '+name)
    a.manuscript.write_text(s);print('Updated data blocks:',a.manuscript)

if __name__=='__main__':main()

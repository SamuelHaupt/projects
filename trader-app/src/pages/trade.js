import React from "react";
import Graphs from '../components/Graphs';
import Info from '../components/Info';
import ManualTrade from '../components/ManualTrade';
import SideBottom from '../components/SideBottom';
import SideTop from '../components/SideTop';
import Footer from '../components/Footer';
import Header from '../components/HeaderS';
 
const Trade = () => {
    return (
    <div className='container'>
      <header className="header">
        <Header/>
      </header>
      <section className='content'>
        <section className='graph-info'>
          <Graphs/>
          <Info/>
        </section>
        <ManualTrade/>
      </section>
      <aside className='sidebar'>
        <SideTop/>
        <SideBottom/>
      </aside>
      <Footer/>
    </div>
    );
};
 
export default Trade;
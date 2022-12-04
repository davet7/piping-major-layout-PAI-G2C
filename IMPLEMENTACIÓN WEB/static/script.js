const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar__menu');

menu.addEventListener('click', function () {
  menu.classList.toggle('is-active');
  menuLinks.classList.toggle('active');
});

let refresh = document.getElementById('refresh');
refresh.addEventListener('click', (_) => {
  location.reload();
});

function matrizdelinea() {
  let numerolinea = document.getElementById('numero').value;
  document.getElementById('matriz').innerHTML = numerolinea;
  let TAGlinea = document.getElementById('TAG').value;
  document.getElementById('TAGdelinea').innerHTML = TAGlinea;
  let equipo1linea = document.getElementById('equipo1').value;
  document.getElementById('equipo1delinea').innerHTML = equipo1linea;
  let equipo2linea = document.getElementById('equipo2').value;
  document.getElementById('equipo2delinea').innerHTML = equipo2linea;
  let diametrolinea = document.getElementById('diametro').value;
  document.getElementById('diametrodelinea').innerHTML = diametrolinea;
  alert(
    '¡La linea ' +
      document.getElementById('numero').value +
      ', ha sido guardada!'
  );
}
